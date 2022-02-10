from Piece import *

class Board:

    
    def __init__(self):
        self.field = [[None for i in range(0,8) ] for j in range(0, 8)]
        self.pieces = []

    ##setters

    def addPiece(self, type: str, team: bool, pos: tuple):

        if(type == Pawn): piece = Pawn(team, pos)
        elif(type == Tower): piece = Tower(team, pos)
        elif(type == Knight): piece = Knight(team, pos)
        elif(type == Bishop): piece = Bishop(team, pos)
        elif(type == Queen): piece = Queen(team, pos)
        elif(type == King): piece = King(team, pos)
        else: return False 

        self.pieces.append(piece)
        return True
    
    def addPieceToField(self):
        for p in self.pieces:
            self.field[p.pos[0]][p.pos[1]] = p
        return True

    def getPieceByPos(self, pos: tuple):
        return self.field[pos[0]][pos[1]]
    
    def setPiecePos(self, pos: tuple, piece: Piece):
        self.field[pos[0]][pos[1]] = piece
        if(piece != None ): piece.pos = pos
        return True

    def capturePiece(self, departure, destiny):
        self.pieces.remove(self.getPieceByPos(destiny))
        self.setPiecePos(destiny, None)
        self.movePiece(departure, destiny)
        return True
    
    def capturePieceEnPassant(self, departure: tuple, destiny: tuple, posPieceCaptured: tuple):
        self.setPiecePos(posPieceCaptured, None)
        self.movePiece(departure, destiny)
        return True

    def movePiece(self, departure: tuple, destiny: tuple): #Essa função não comporta captura
        piece = self.getPieceByPos(departure)
        self.setPiecePos(departure, None) #seta vazio na posição de departure da piece
        self.setPiecePos(destiny, piece) #seta piece na posição de chegada
        return True
    
    def checkTypePiece(self, piece, type):
        if(type == 'peao'): return isinstance(piece, Pawn)
        if(type == 'torre'): return isinstance(piece, Tower)
        if(type == 'cavalo'): return isinstance(piece, Knight)
        if(type == 'bispo'): return isinstance(piece, Bishop)
        if(type == 'rei'): return isinstance(piece, Queen)
        if(type == 'rainha'): return isinstance(piece, King)
    
    def getPieceTeamByPos(self, pos:tuple):
        piece = self.getPieceByPos(pos)
        if piece == None: return None
        return piece.team
