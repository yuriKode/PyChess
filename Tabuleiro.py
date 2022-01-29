from Pedra import *

class Tabuleiro:

    def __init__(self):
        self.campo = [[None for i in range(0,8) ] for j in range(0, 8)]
        self.pedras = []

    ##setters

    def add_pedra(self, tipo: str, time: bool, pos: tuple):

        if(tipo == 'peao'): pedra = Peao(time, pos)
        elif(tipo == 'torre'): pedra = Torre(time, pos)
        elif(tipo == 'cavalo'): pedra = Cavalo(time, pos)
        elif(tipo == 'bispo'): pedra = Bispo(time, pos)
        elif('Rainha'): pedra = Rainha(time, pos)
        elif('Rei'): pedra = Rei(time, pos)
        else: return False # pedra inválida

        self.pedras.append(pedra)

        return True
    
    def add_pedras_ao_campo(self):
        for p in self.pedras:
            self.campo[p.pos[0]][p.pos[1]] = p
        return True

    ##getters

    def get_pedra_by_pos(self, pos: tuple):
        return self.campo[pos[0]][pos[1]]
    
    def set_pedra_by_pos(self, pos: tuple, piece: Pedra):
        self.campo[pos[0]][pos[1]] = piece
        if(piece != None ): piece.pos = pos
        return True

    def capturaPedra(self, partida, destino):
        self.set_pedra_by_pos(destino, None)
        self.movePedra(partida, destino)
        return True

    def movePedra(self, partida: tuple, destino: tuple): #Essa função não comporta captura
        piece = self.get_pedra_by_pos(partida)
        self.set_pedra_by_pos(partida, None) #seta vazio na posição de partida da pedra
        self.set_pedra_by_pos(destino, piece) #seta pedra na posição de chegada
        return True
    
    def checkTypePiece(self, piece, tipo):
        if(tipo == 'peao'): return isinstance(piece, Peao)
        if(tipo == 'torre'): return isinstance(piece, Torre)
        if(tipo == 'cavalo'): return isinstance(piece, Cavalo)
        if(tipo == 'bispo'): return isinstance(piece, Bispo)
        if(tipo == 'rei'): return isinstance(piece, Rainha)
        if(tipo == 'rainha'): return isinstance(piece, Rei)
    
    def getPieceTime(self, pos:tuple):
        piece = self.get_pedra_by_pos(pos)
        if piece == None: return None
        return piece.time


    #funções edit (movimento)

    #funções deleção (captura)

    ##Parei aqui https://docs.python.org/3.8/tutorial/inputoutput.html
    ## Se quiser uma api de matrix use numpy

