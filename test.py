import math

def LinearEquation(x1, y1, x2, y2):
    """" General Format Ax + By = C"""

    A = y1 - y2
    B = x2 - x1
    C = (x1*y2 - x2*y1)

    return lambda x, y: A*x + B*y + C

def pawnSubEquation(x, y, x1, y1, x2, y2):

    distance = math.floor(math.dist((x1, y1), (x, y)))

    if(distance == 1) :
        g = LinearEquation(x1, y1, x2, y2)
        return g(x, y)
    else: return 1

def pawnEquation(x1, y1):
    x2 = x1 ; y2 = y1 + 1  # vertical movement
    return lambda x, y: pawnSubEquation(x, y, x1, y1, x2, y2)

x1 = 5; y1 = 3
f = pawnEquation(x1, y1)


for i in range(0, 8):
    for j in range (0, 8):
        print("f(" + str(i) + ", " + str(j) + ") = " + str(f(i, j)))

