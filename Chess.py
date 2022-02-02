from Board import Board
from Player import Player
from Movement import Movement
from ReverseMovement import ReverseMovement
from Piece import *
from ScoreSheet import ScoreSheet
import re

class Chess:
    """Criando um jogo de xadrez"""

    def __init__(self):
        self.board = Board()
        self.jogadores = list
        self.scoreSheet = ScoreSheet(self)

    def createGame(self): # Normal variations

        for team in [0, 1]:
            y = 5* team  + 1
            for x in range(0,8): self.board.addPiece(Pawn, team, (x,y))
            y = team * 7
            for i in range(0,2):
                x = i * 7
                self.board.addPiece(Tower, team, (x,y))
            for i in range(0,2):
                x = 5 * i + 1
                self.board.addPiece(Knight, team, (x,y))
            for i in range(0,2):
                x = 3*i + 2
                self.board.addPiece(Bishop, team, (x,y))
            x = 3
            self.board.addPiece(Queen, team, (x,y))
            x = 4
            self.board.addPiece(King, team, (x,y))

        self.board.addPieceToField()
        return True

    def see(self):

        for y in reversed(range(0, 8)):
            print('   ', end = '')
            print('-' * 33)
            print(str(y + 1) + ' ', end = '')
            for x in range(0, 8):
                print(' | ', end = '')
                piece = self.board.getPieceByPos((x,y))
                if(piece == None):
                    print(' ', end = '')
                else:
                    print(piece.img[not piece.team], end = '')

                if(x >= len(range(0, 8)) - 1):
                    print(' |')

        ## fechamento última linha
        print('   ', end = '')
        print('-' * 33)
        # printa nome das colunas
        print('   ', end = '')
        for i in range(0, 8):
            print('  ', end = '')
            print(chr(ord('a') + i), end = '')
            if(i < len(range(0, 8)) - 1):
                print(' ', end = '')
            else:
                print()

    def formatCoordsToHumans(self, coord: tuple):
        col = str(chr(int(coord[0]) + ord('a')))
        lin = str(int(coord[1]) + 1)
        return (col + lin)

    def formatCoordsToMachine(self, col: chr, lin: chr):
        if(col != None): c = ord(col) - ord('a')
        else: c = None
        if(lin != None): l = int(lin) - 1
        else: l = None
        return (c, l)   
    
    def defineCapture(self, capture):
        if(capture == 'x'): return True
        else: return False

    def definePromotion(self, promotion):
        pass
        return None

    def formatMatches(self, matches):

        formatted_matches = {}
        
        typePiece = Piece.getTypePiece(matches['letterTypePiece'])
        posDestiny = self.formatCoordsToMachine(matches['xDestiny'], matches['yDestiny'])
        posAmbiguity = self.formatCoordsToMachine(matches['xAmbiguity'], matches['yAmbiguity'])
        capture = self.defineCapture(matches['capture'])
        typePiecePromotion = self.definePromotion(matches['promotion'])
        isCheck = matches['check']
        isCheckmate = matches['checkmate']

        formatted_matches = {'typePiece': typePiece,
                            'posDestiny': posDestiny,
                            'posAmbiguity': posAmbiguity,
                            'capture': capture,
                            'typePiecePromotion': typePiecePromotion,
                            'isCheck': isCheck,
                            'isCheckMate': isCheckmate
                            }

        return formatted_matches
    
    def readMovement(self, team: bool(), string: str()):
        match = re.fullmatch(r"(?P<letterTypePiece>[KQRBN])?(?P<ambiguity>(?P<xAmbiguity>[a-h])?(?P<yAmbiguity>[1-8])?)?(?P<capture>x)?(?P<destiny>(?P<xDestiny>[a-h])(?P<yDestiny>[1-8]))(?P<promotion>(?(letterTypePiece)|[QRBN]))?((?P<check>\+)?|(?P<checkmate>#))", string)
        if(match):
            matches = match.groupdict()
            formatted_matches = self.formatMatches(matches)
            reverseMovement =  ReverseMovement(team, formatted_matches, self.board, self.scoreSheet)
            answer = reverseMovement.findReverseMovement()

            if(answer['status'] == True): self.scoreSheet.saveMovement(string)
            
            return answer
        else: return {'status': False, 'msg': 'Your movement is formatted incorrectly !'}



##Contruir um catálogo de erros