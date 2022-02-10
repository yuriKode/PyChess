class Piece:

    def __init__(self, team: bool, pos: tuple, img: list =  None, lamb_func: str = None ):
        self.team = team  # 0 => branco , 1 => preto
        self.pos = pos  # x => horizontal, y => vertical (limites de 0 a 7)
        self.lamb_func = lamb_func #função de movimento da peça
        self.img = img # string contendo img da peça

    def getTypePiece(letterTypePiece):
        if(letterTypePiece == None): return Pawn
        elif (letterTypePiece == 'R'): return Tower
        elif(letterTypePiece == 'N'): return Knight
        elif(letterTypePiece == 'B'): return Bishop
        elif(letterTypePiece == 'Q'): return Queen
        elif(letterTypePiece == 'K'): return King
        else: return None

class Pawn(Piece):

    def __init__(self, team, pos, img = ['\u2659', '\u265F'] , lamb_func = None):
        super().__init__(team, pos, img, lamb_func)
    
    def __str__(self) -> str:
        return "Pawn"

class Tower(Piece):

    def __init__(self, team, pos, img = ['\u2656', '\u265C'], lamb_func = None ):
        super().__init__(team, pos, img, lamb_func)
    
    def __str__(self) -> str:
        return "Rook"

class Knight(Piece):

    def __init__(self, team, pos, img = ['\u2658', '\u265E'], lamb_func = None ):
        super().__init__(team, pos, img, lamb_func)

class Bishop(Piece):
    
    def __init__(self, team, pos, img = ['\u2657', '\u265D'], lamb_func = None ):
        super().__init__(team, pos, img, lamb_func)

class Queen(Piece):

    def __init__(self, team, pos, img = ['\u2655', '\u265B'], lamb_func = None ):
        super().__init__(team, pos, img, lamb_func)

class King(Piece):

    def __init__(self, team, pos, img = ['\u2654', '\u265A'], lamb_func = None ):
        super().__init__(team, pos, img, lamb_func)