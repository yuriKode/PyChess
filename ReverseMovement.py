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

    def isInTheBoard(self, pos: tuple):
        if(self.LIM_MIN <= pos[0] <= self.LIM_MAX 
        and self.LIM_MIN <= pos[1] <= self.LIM_MAX): return True
        else: return False

    def findReverseMovement(self):

        if(self.typePiece == Pawn): answer = self.findReversedMovement()
        elif(self.typePiece == Tower): answer = self.findReversedMovement()
        elif(self.typePiece == Bishop): answer = self.findReversedMovement()
        elif(self.typePiece == Knight): answer = self.findReversedMovement()
        elif(self.typePiece == Queen): answer = self.findReversedMovement()
        elif(self.typePiece == King):
            pass
        else: answer = {'status': False, 'msg': 'Invalid Piece !'}

        if(answer['status'] == True): 
            self.doMovement(answer['mov'])
            return {'status': True, 'mov': answer['mov']}
        else: return answer

    def doMovement(self, mov):
        
        if(mov['capture'] == True):
            if(('enPassant' in mov) and mov['enPassant'] == True):
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
    
    def findReversedMovement(self):

        possiblePieces = self.findAllPiecesForThatMovement()
        legalMovements = self.findLegalMovements(possiblePieces)
        disambiguateMovement = self.disambiguateMovement(legalMovements)

        if(len(legalMovements) != 0):
            if(disambiguateMovement['piece'] != None):
                pieceMoving = disambiguateMovement['piece']
                mov = {'piece': pieceMoving, 
                        'team': self.team, 
                        'from': pieceMoving.pos, 
                        'to': self.posDestiny, 
                        'capture': self.capture}
                return {'status': True, 'mov': mov}
            else:
                return {'status': False, 'msg': disambiguateMovement['msg']}
        else:
            return {'status': False, 'msg': 'No movement like that is possible!'}

    def findAllPiecesForThatMovement(self):
        
        allPieces = self.board.pieces

        if(self.typePiece == Pawn): functionsDestiny = Movement.makePawnFunctions(self.posDestiny, self.capture, 'fromDestiny', self.team)
        elif(self.typePiece == Tower): functionsDestiny = Movement.makeTowerFunctions(self.posDestiny)
        elif(self.typePiece == Bishop): functionsDestiny = Movement.makeBishopFunctions(self.posDestiny)
        elif(self.typePiece == Knight): functionsDestiny = Movement.makeKnightFunctions(self.posDestiny)
        elif(self.typePiece == Queen): functionsDestiny = Movement.makeQueenFunctions(self.posDestiny)

        possiblePieces = []
        for f in functionsDestiny:
           for piece in allPieces:
               if (piece.team == self.team and isinstance(piece, self.typePiece)):
                    xPiece = piece.pos[0]; yPiece = piece.pos[1]
                    if (f(xPiece, yPiece) == 0):
                        possiblePieces.append(piece)

        return possiblePieces
    
    def findLegalMovements(self, possiblePieces: list):

        legalMovements = []
        allPieces = self.board.pieces
        for p in possiblePieces:

            if(self.typePiece == Pawn):
                functions = Movement.makePawnFunctions(p.pos, self.capture, 'fromPiece', self.team)
                legalMovement = Movement.testPoints(functions, p, self.posDestiny, allPieces, self.team, self.capture)
            elif(self.typePiece == Tower): 
                functions = Movement.makeTowerFunctions(p.pos)
                legalMovement = Movement.testPoints(functions, p, self.posDestiny, allPieces, self.team, self.capture)
            elif (self.typePiece == Bishop): 
                functions = Movement.makeBishopFunctions(p.pos)
                legalMovement = Movement.testPoints(functions, p, self.posDestiny, allPieces, self.team, self.capture)
            elif (self.typePiece == Knight): 
                functions = Movement.makeKnightFunctions(p.pos)
                legalMovement = Movement.testPointKnight(functions, p, self.posDestiny, allPieces, self.team, self.capture)
            elif (self.typePiece == Queen): 
                functions = Movement.makeQueenFunctions(p.pos)
                legalMovement = Movement.testPoints(functions, p, self.posDestiny, allPieces, self.team, self.capture)
            
            if(len(legalMovement) != 0): legalMovements.append(legalMovement)

        return legalMovements

    def disambiguateMovement(self, legalMovements):

        if(len(legalMovements) != 0):
            legalPieces = [l['piece'] for mov in legalMovements for l in mov]
            ans = self.disambiguatePieces(legalPieces)
            return ans
        else:
            return None
    
    def disambiguatePieces(self, possiblePieces: list) -> dict:

        numberPossiblePieces = len(possiblePieces)
        if (numberPossiblePieces == 1): pieceMoving = possiblePieces[0]; msg = 'Ok'
        if (numberPossiblePieces > 1):
            newPossiblePieces = possiblePieces.copy()
            if(self.posAmbiguity != (None, None)):
                for i in [0, 1]:
                    if(self.posAmbiguity[i] != None):
                        for p in possiblePieces:
                            if (self.posAmbiguity[i] != p.pos[i]):
                                newPossiblePieces.remove(p)
                newNumberPossiblePieces = len(newPossiblePieces)
                if(newNumberPossiblePieces == 1): pieceMoving = newPossiblePieces[0]
                else: pieceMoving = None; msg = 'Movement not disambiguated!'
            else: pieceMoving = None; msg = 'Ambiguos movement!'
        
        return {'piece': pieceMoving, 'msg': msg}

    