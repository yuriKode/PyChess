import os
from datetime import datetime
import re

class ScoreSheet:

    def __init__(self, chess):
        self.makeFile()
        self.countMoves = 0
        self.countRounds = 0
        self.chess = chess

    def makeFile(self):
        try:
            os.mkdir('games')
            print('Directory "games" created!')
        except FileExistsError:
            print('Directory already created!')

        self.filename = 'games/' + str(datetime.now()) + '.txt'
        
        try:
           with open(self.filename, 'x'): pass
        except OSError:
            print('Failed to create the Score Sheet')
        else:
            print('Score Sheet created!')

        # https://docs.python.org/3.8/library/functions.html#open
        

    def saveMovement(self, string: str):
        self.countMoves += 1
        try:
            with open(self.filename, 'a') as f:
                if(self.countMoves%2 != 0):
                    self.countRounds += 1
                    f.write(str(self.countRounds) + '. ' + string + ' ')
                else:
                    f.write(string + '\n')
        except OSError:
            print('Failed to update the Score Sheet')
        else:
            print('Score Sheet updated')

    def getLastMovement(self, team):
        try:
           with open(self.filename, 'r') as f:
               for line in f: pass
               lastLine = line
        except OSError:
            print('Failed to read the last movement')
        else:
            print('Last movement read sucessfully')

        if(team == False):
            match = re.search(r"(?<= )((?P<xMovement>[a-h])(?P<yMovement>[1-8]))(?= )", lastLine)
        else:
            match = re.search(r"(?<= )((?P<xMovement>[a-h])(?P<yMovement>[1-8]))(?=\n)", lastLine)
        
        if(match):
            mov = self.chess.formatCoordsToMachine(match['xMovement'], match['yMovement'])
            return {'status': True, 'mov': mov}
        else:
            return {'status': False, 'msg': "Last movement not found"}
