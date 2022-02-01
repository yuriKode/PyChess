from Piece import *
from Board import Board
from Movement import Movement

class ReverseMovement(Movement):

    LIM_MIN = 0
    LIM_MAX = 7

    def __init__(self, team: bool, formattedMatches, board: Board):
        self.team = team
        self.typePiece = formattedMatches['typePiece']
        self.posAmbiguity = formattedMatches['posAmbiguity']
        self.capture = formattedMatches['capture']
        self.posDestiny = formattedMatches['posDestiny']
        self.typePiecePromotion = formattedMatches['typePiecePromotion']
        self.isCheck = formattedMatches['isCheck']
        self.isCheckMate = formattedMatches['isCheckMate']
        self.board = board

    def isInTheBoard(self, pos):
        if(self.LIM_MIN <= pos[0] <= self.LIM_MAX 
        and self.LIM_MIN <= pos[1] <= self.LIM_MAX): return True
        else: return False

    def findReverseMovement(self):

        if(self.typePiece == Pawn): answer = self.findReversedPawnMovement()
        elif(self.typePiece == Tower): 
            pass
        elif(self.typePiece == Bishop):
            pass
        elif(self.typePiece == Knight):
            pass
        elif(self.typePiece == Queen):
            pass
        elif(self.typePiece == King):
            pass
        else: answer = {'status': False, 'msg': 'Invalid Piece !'}

        if(answer['status'] == True): 
            self.doMovement(answer['mov'])
            return {'status': True, 'msg': 'Movement Done!!'}
        else: return answer

    def findReversedPawnMovement(self):

        possibleMovements = []
        if(not self.team): inverter = 1; rankException = 1
        else: inverter = -1 ; rankException = 6

        if(self.capture == True):
            for i in [1,2]:
                xPartial = self.posDestiny[0] + pow(-1, i)
                yPartial = self.posDestiny[1] - 1 * inverter
                posPartial = (xPartial, yPartial)
                if(self.isInTheBoard(posPartial)):
                    piecePartial = self.board.getPieceByPos(posPartial)
                    if(piecePartial == None): continue
                    else:
                        if(piecePartial.team == self.team and isinstance(piecePartial, Pawn)):
                            pieceDestiny =  self.board.getPieceByPos(self.posDestiny)
                            if(pieceDestiny != None):
                                if(pieceDestiny.team == (not self.team)): 
                                    possibleMovements.append({'from': posPartial, 
                                                                'to': self.posDestiny, 
                                                                'capture': True})
        else:
            xPartial = self.posDestiny[0]
            for i in [1,2]:
                yPartial = self.posDestiny[1] - i * inverter
                posPartial = (xPartial, yPartial)
                if(i == 2 and yPartial != rankException): break
                if(self.isInTheBoard(posPartial)):
                    piecePartial = self.board.getPieceByPos(posPartial)
                    if(piecePartial == None): continue
                    else:
                        if(piecePartial.team == self.team and isinstance(piecePartial, Pawn)):
                            pieceDestiny =  self.board.getPieceByPos(self.posDestiny)
                            if(pieceDestiny == None): 
                                possibleMovements.append({'from': posPartial, 
                                                            'to': self.posDestiny,
                                                            'capture': False})
                        break

        numberPossibleMovements = len(possibleMovements)

        if(numberPossibleMovements == 0): return {'status': False, 'msg': 'Impossible Movement!'}
        elif (numberPossibleMovements == 1): 
            if(self.posAmbiguity != (None, None)): 
                return {'status': False, 'msg': 'Your movement is not ambiguos!'}
            return {'status': True , 'mov': possibleMovements[0]}
        else:
            possibleMovementsFiltered = possibleMovements.copy()
            if(self.posAmbiguity != (None, None)):
                for i in [0, 1]:
                    if(self.posAmbiguity[i] != None):
                        for mov in possibleMovements:
                            if (self.posAmbiguity[i] != mov['from'][i]):
                                possibleMovementsFiltered.remove(mov)

                if(len(possibleMovementsFiltered) == 1): return {'status': True, 'mov': possibleMovementsFiltered[0]}
                else: return {'status': False, 'msg': 'Movement not disambiguated'}
            else: return {'status': False, 'msg': 'Ambiguos Movement!'}

    

    def doMovement(self, mov):
        
        if(mov['capture'] == True): self.board.capturePiece(mov['from'], mov['to'])
        else: self.board.movePiece(mov['from'], mov['to'])
        