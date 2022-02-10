import os
from datetime import datetime
import re
import csv

class ScoreSheet:

    def __init__(self, chess):
        self.makeFile()
        self.countMoves = 0
        self.countRounds = 0
        self.chess = chess

    def makeFile(self):

        self.directory = 'games/' + str(datetime.now())
        try:
            os.mkdir(self.directory)
            print('Directory created!')
        except FileExistsError:
            print('Directory already created!')

        self.filename = 'Algebraic_Notation.txt'
        self.filename2 = 'Detailed.csv'
        
        try:
           with open(self.directory + '/' + self.filename, 'x'): pass
           with open(self.directory + '/' + self.filename2, 'x', encoding='UTF8', newline=''): pass
        except OSError:
            print('Failed to create the Score Sheet')
        else:
            print('Score Sheet created!')

        # https://docs.python.org/3.8/library/functions.html#open
        

    def saveMovement(self, string: str, details: dict):
        self.countMoves += 1
        try:
            with open(self.directory + '/' + self.filename, 'a') as f:
                if(self.countMoves%2 != 0):
                    self.countRounds += 1
                    f.write(str(self.countRounds) + '. ' + string + ' ')
                else:
                    f.write(string + '\n')
        except OSError:
            print('Failed to update the Score Sheet')
        else:
            print('Score Sheet updated')

        if(self.countMoves == 1): data = [['Round', 'Team', 'Piece' , 'From', 'To', 'Capture']]
        else: 
            if(self.countMoves%2 == 0): round = str(self.countRounds)
            else: round = ''
            
            data = [[round,
                    self.chess.formatTeamToHumans(details['team']),
                    str(details['piece']), 
                    self.chess.formatCoordsToHumans(details['from']), 
                    self.chess.formatCoordsToHumans(details['to']), 
                    str(details['capture'])
            ]]
        
        try:
            with open(self.directory + '/' + self.filename2, 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(data)
        except OSError:
            print('Failed to update the Detailed Sheet')
        else:
            print('Detailed Sheet updated')

    def findLastMovement(self, movFrom, movTo, team):

        with open(self.directory + '/' + self.filename2, 'r') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if(((count == self.countMoves - 2) or (count == self.countMoves - 1)) and (row['Team'] == team)):
                    if(row['From'] == movFrom and row['To'] == movTo):
                        return True
                    else:
                        return False
                count += 1
                


