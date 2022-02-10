from Piece import *
from Board import Board
import math

LIM_MIN = 0
LIM_MAX = 7

class Movement:

    def __init__(self):
        pass

    def constructMove(self, typePiece, departure: tuple, destiny: tuple, team: bool):
        pass
    
    def LinearEquation(x1, y1, x2, y2):
        """" General Format Ax + By = C"""

        A = y1 - y2
        B = x2 - x1
        C = (x1*y2 - x2*y1)

        return lambda x, y: A*x + B*y + C
    
    def isMoving(x, y, xP, yP):
        if(x != xP or y != yP): return True
        else: return False

    def isInTheBoard(x, y):
        if(LIM_MIN <= x <= LIM_MAX and LIM_MIN <= y <= LIM_MAX): return True
        else: return False

    def makePawnFunction(xP, yP):
        
        functions = []
        x2 = xP; y2 = yP + 1  # vertical movement
        functions.append(Movement.LinearEquation(xP, yP, x2, y2))
        x2 = xP + 1 # positive diagonal
        functions.append(Movement.LinearEquation(xP, yP, x2, y2))
        x2 = xP - 1 # negative diagonal
        functions.append(Movement.LinearEquation(xP, yP, x2, y2))

        return functions
    
    def makeTowerFunctions(posP):
        functions = []
        xP = posP[0]; yP = posP[1]
        x2 = xP; y2 = yP - 1  # known point of the vertical
        functions.append(Movement.LinearEquation(xP, yP, x2, y2))
        x2 = xP - 1; y2 = yP  # known point of the horizontal
        functions.append(Movement.LinearEquation(xP, yP, x2, y2))

        return functions
    
    def testPoints(functions, piece, destiny, allPieces, myTeam, capture):
        
        legalMovements = []
        x = destiny[0] ; y = destiny[1]
        xP = piece.pos[0]; yP = piece.pos[1]
        if(Movement.isInTheBoard(x, y) and Movement.isMoving(x, y, xP, yP)):
            for f in functions:
                if(f(x, y) == 0):
                    arrayIntersection = []
                    for p in allPieces:
                        if (p != piece):
                            px = p.pos[0]; py = p.pos[1]
                            if(((xP <= px <= x) or (x <= px <= xP)) and
                            ((yP <= py <= y) or (y <= py <= yP)) and
                            (f(px, py) == 0)):
                                arrayIntersection.append(p)

                    if(len(arrayIntersection)== 0): 
                        legalMovements.append({'team': myTeam,
                                                'piece': piece,
                                                'from': piece.pos, 
                                                'to': destiny,
                                                'capture': False })
                    else:
                        distances = []
                        for p in arrayIntersection:
                            px = p.pos[0]; py = p.pos[1]
                            distances.append(math.sqrt((px - xP)**2 + (py - yP)**2))

                        minDistance = min(distances)
                        min_index = distances.index(minDistance)
                        pieceIntersect = arrayIntersection[min_index]
                        distanceMyMovement = math.sqrt((xP - x)**2 + (yP - y)**2)
                        if(distanceMyMovement == minDistance and pieceIntersect.team != myTeam and capture == True): 
                            legalMovements.append({'team': myTeam,
                                                'piece': piece,
                                                'from': piece.pos, 
                                                'to': destiny,
                                                'capture': True })
                    
            
        return legalMovements

"""
A ideia vai ser fazer o reverso de todas aquelas funções que usei no algoritmo de álgebra linear.
Ao invés de encontrar os pontos da função, iremos tentar encontrar a origem, seja, na linha, no círculo
ou no quadrado.
Estudar função do peão melhor.

"""