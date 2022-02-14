from Piece import *
from Board import Board
import math

LIM_MIN = 0
LIM_MAX = 7

class Movement:

    def __init__(self):
        pass
    
    def LinearEquation(x1, y1, x2, y2):
        """" General Format Ax + By = C"""

        A = y1 - y2
        B = x2 - x1
        C = (x1*y2 - x2*y1)

        return lambda x, y: A*x + B*y + C
    
    def circularEquation(a, b, x, y):
        """ General Form (x - a)² + (y - b)² - r² = 0 
            Where (a, b) is the point at the center
            and (x, y) a point of the circle 
        """
        r = math.sqrt((x - a)**2 + (y - b)**2)
        return lambda x, y: round((x - a)**2 + (y - b)**2 - r**2, 4)

    
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
    
    def makeTowerFunctions(pos):
        functions = []
        xP = pos[0]; yP = pos[1]
        x2 = xP; y2 = yP - 1  # known point of the vertical
        functions.append(Movement.LinearEquation(xP, yP, x2, y2))
        x2 = xP - 1; y2 = yP  # known point of the horizontal
        functions.append(Movement.LinearEquation(xP, yP, x2, y2))

        return functions
    
    def makeBishopFunctions(pos):
        functions = []
        xP = pos[0]; yP = pos[1]
        x2 = xP + 1; y2 = yP + 1  # known point of the positive diagonal
        functions.append(Movement.LinearEquation(xP, yP, x2, y2))
        x2 = xP - 1; y2 = yP + 1  # known point of the negative diagonal
        functions.append(Movement.LinearEquation(xP, yP, x2, y2))

        return functions
    
    def makeKnightFunctions(pos):
        functions = []
        x = pos[0] + 1
        y = pos[1] + 2
        f = Movement.circularEquation(pos[0], pos[1], x, y)
        functions.append(f)
        return functions

    def makeQueenFunctions(pos):

        functions = []
        towerFunctions = Movement.makeTowerFunctions(pos)
        bishopFunctions = Movement.makeBishopFunctions(pos)
        for f in towerFunctions:
            functions.append(f)
        for f in bishopFunctions:
            functions.append(f)

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

    def testPointKnight(functions, piece, destiny, allPieces, myTeam, capture):

        legalMovements = []
        x = destiny[0] ; y = destiny[1]
        xP = piece.pos[0]; yP = piece.pos[1]
        if(Movement.isInTheBoard(x, y) and Movement.isMoving(x, y, xP, yP)):
            for f in functions:
                if(f(x, y) == 0):
                    arrayIntersection = []
                    for p in allPieces:
                        px = p.pos[0]; py = p.pos[1]
                        if(px == x and py == y):
                            arrayIntersection.append(p)

                if(len(arrayIntersection)== 0):
                    legalMovements.append({'team': myTeam,
                                                'piece': piece,
                                                'from': piece.pos, 
                                                'to': destiny,
                                                'capture': False })
                else:
                    pieceIntersect = arrayIntersection[0]
                    if(pieceIntersect.team != myTeam and capture == True):
                        legalMovements.append({'team': myTeam,
                                                'piece': piece,
                                                'from': piece.pos, 
                                                'to': destiny,
                                                'capture': True })
                    
        return legalMovements