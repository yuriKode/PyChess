from Piece import *
from Board import Board
from Movement import Movement
from ScoreSheet import ScoreSheet


class ReverseMovement(Movement):

    LIM_MIN = 0
    LIM_MAX = 7

    def __init__(self, team: bool, formattedMatches, board: Board, scoreSheet: ScoreSheet):
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
                                                                'capture': True,
                                                                'enPassant': False})
                            else:
                                if ((self.team == True and self.posDestiny[1] == 2)or #try enpassant
                                    (self.team == False and self.posDestiny[1] == 5)):
                                    lastMovement = self.scoreSheet.getLastMovement(not self.team)
                                    if(lastMovement['status'] == True):
                                        if((lastMovement['mov'][0] == self.posDestiny[0]) and
                                            ((lastMovement['mov'][1] == 4 and self.team == False) or 
                                            (lastMovement['mov'][1] == 3 and self.team == True ))):
                                            possibleMovements.append({'from': posPartial, 
                                                                    'to': self.posDestiny, 
                                                                    'capture': True,
                                                                    'enPassant': True,
                                                                    'posPieceCaptured': lastMovement['mov']})
                                    
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
        
        if(mov['capture'] == True):
            if(mov['enPassant'] == True):
                self.board.capturePieceEnPassant(mov['from'], mov['to'], mov['posPieceCaptured'])
            else: self.board.capturePiece(mov['from'], mov['to'])
        else: self.board.movePiece(mov['from'], mov['to'])

    

    def findReversedPawnMovement2(self,):

        #Algorithm for pawn capture

        #What we have?
        #The team of the movement team = 0 -> step = -1 ; team = 1 -> step = 1
        #The destiny position
        #The file of departure of the pawn

        #Check if is capture and if we have the file of departure of the pawn
            #Go back 1 rank - Partial position (file of departure, destinyRank + step)
            #Check if Partial position is in the Board
                #Is there a pawn of my team in this position?
                    #Is there a piece of the opposite team in the destiny position?
                        #Enable movement
                    #Else, if is empty check enPassant
                        #Check if the movement (destiny) was made before by the adversary
                            # Check if the last movement was (fileDestiny, Destinyrank - step)
                                #Enable movement

        
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
                        possibleMovements.append({'from': posPartial, 'to': self.posDestiny, 'capture': True, 'enPassant': False})
                else: #Check enPassant
                    #self.constructMove()
                    #self.scoreSheet.wasThisMovementMadeBefore()
                    #To Continue with the En Passant Logic
                    pass