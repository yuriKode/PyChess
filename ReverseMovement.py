from Piece import *
from Movement import Movement

class ReverseMovement(Movement):

    LIM_MIN = 0
    LIM_MAX = 7

    def __init__(self, team: bool, formattedMatches, board, scoreSheet, chess):
        self.team = team
        self.typePiece = formattedMatches['typePiece']
        self.posAmbiguity = formattedMatches['posAmbiguity']
        self.capture = formattedMatches['capture']
        self.posDestiny = formattedMatches['posDestiny']
        self.typePiecePromotion = formattedMatches['typePiecePromotion']
        self.isCheck = formattedMatches['isCheck']
        self.isCheckMate = formattedMatches['isCheckMate']
        self.board = board
        self.scoreSheet = scoreSheet
        self.chess = chess

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
            return {'status': True, 'mov': answer['mov']}
        else: return answer

    def doMovement(self, mov):
        
        if(mov['capture'] == True):
            if(mov['enPassant'] == True):
                self.board.capturePieceEnPassant(mov['from'], mov['to'], mov['posPieceCaptured'])
            else: self.board.capturePiece(mov['from'], mov['to'])
        else: self.board.movePiece(mov['from'], mov['to'])

    

    def findReversedPawnMovement(self):
        
        possibleMovements = []
        if(not self.team): inverter = 1; rankException = 1
        else: inverter = -1 ; rankException = 6

        if(self.capture == True and self.posAmbiguity[0] != None):
            xPartial = self.posAmbiguity[0]
            yPartial = self.posDestiny[1] - 1 * inverter
            posPartial = (xPartial, yPartial)
            piecePartial = self.board.getPieceByPos(posPartial)
            if(piecePartial != None and piecePartial.team == self.team and isinstance(piecePartial, Pawn)):
                pieceDestiny = self.board.getPieceByPos(self.posDestiny)
                if(pieceDestiny != None):
                    if(pieceDestiny.team == (not self.team)):
                        possibleMovements.append({'team': self.team, 'piece': piecePartial, 'from': posPartial, 'to': self.posDestiny, 'capture': True, 'enPassant': False})
                else: #Check enPassant
                    
                    yEnPassantDestiny = int(1.5 * inverter + 3.5)
                    if(self.posDestiny[1] == yEnPassantDestiny):
                        xEnPassant = self.posDestiny[0]
                        yEnPassant = self.posDestiny[1] - 1*inverter
                        coordEnPassant = (xEnPassant, yEnPassant)
                        pieceEnPassant = self.board.getPieceByPos(coordEnPassant)
                        if(pieceEnPassant != None):
                            if(pieceEnPassant.team == (not self.team) and isinstance(pieceEnPassant, Pawn)):
                                yEnPassant2 = yEnPassant + 2*inverter
                                coordEnPassant2 = (xEnPassant, yEnPassant2)
                                movFrom = self.chess.formatCoordsToHumans(coordEnPassant2)
                                movTo = self.chess.formatCoordsToHumans(coordEnPassant)
                                team = self.chess.formatTeamToHumans((not self.team))
                                lastMov = self.scoreSheet.findLastMovement(movFrom, movTo, team)
                                if(lastMov): possibleMovements.append({'team': self.team, 
                                                                        'piece': piecePartial, 
                                                                        'from': posPartial, 
                                                                        'to': self.posDestiny, 
                                                                        'capture': True, 
                                                                        'enPassant': True,
                                                                        'posPieceCaptured': coordEnPassant})
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
                                possibleMovements.append({'team': self.team,
                                                            'piece': piecePartial,
                                                            'from': posPartial, 
                                                            'to': self.posDestiny,
                                                            'capture': False})
                        break

        numberPossibleMovements = len(possibleMovements)

        if(numberPossibleMovements == 0): 
            if(self.posAmbiguity[0] == None) and (self.capture): return {'status': False, 'msg': 'Type the file of pawn'}
            return {'status': False, 'msg': 'Impossible Movement!'}      
        elif (numberPossibleMovements == 1): return {'status': True , 'mov': possibleMovements[0]}
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
            