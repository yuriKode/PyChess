from nis import match
from operator import truediv
from Tabuleiro import Tabuleiro
from Jogador import Jogador
import re

class Xadrez:
    """Criando um jogo de xadrez"""

    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.jogadores = list

    def cria_jogo(self):

        for time in range(0,2):
        ##Peoes
            y = 5* time  + 1 ## segundo e penúltimo rank
            for x in range(0,8):
                self.tabuleiro.add_pedra('peao', time, (x,y))
            ##primeiro e último rank
            y = time * 7
            ##Torres
            for i in range(0,2):
                x = i * 7
                self.tabuleiro.add_pedra('torre', time, (x,y))
            ##Cavalos
            for i in range(0,2):
                x = 5 * i + 1
                self.tabuleiro.add_pedra('cavalo', time, (x,y))
            ##Bispos
            for i in range(0,2):
                x = 3*i + 2
                self.tabuleiro.add_pedra('bispo', time, (x,y))
            ##Rainha
            x = 3
            self.tabuleiro.add_pedra('rainha', time, (x,y))
            ##Rei
            x = 4
            self.tabuleiro.add_pedra('rei', time, (x,y))

        self.tabuleiro.add_pedras_ao_campo()
        return True

    def ver(self):

        for y in reversed(range(0, 8)):
            print('   ', end = '')
            print('-' * 33)
            print(str(y + 1) + ' ', end = '')
            for x in range(0, 8):
                print(' | ', end = '')
                pedra = self.tabuleiro.get_pedra_by_pos((x,y))
                if(pedra == None):
                    print(' ', end = '')
                else:
                    print(pedra.img[pedra.time], end = '')

                if(x >= len(range(0, 8)) - 1):
                    print(' |')

        ## fechamento última linha
        print('   ', end = '')
        print('-' * 33)
        # printa nome das colunas
        print('   ', end = '')
        for i in range(0, 8):
            print('  ', end = '')
            print(chr(ord('a') + i), end = '')
            if(i < len(range(0, 8)) - 1):
                print(' ', end = '')
            else:
                print()

    
    def checkLims(self, xParcial, yParcial): #Checa se possível coordenada está no bordo se não retorna impossível
        if xParcial >= 0 and xParcial <= 7: 
            if yParcial >= 0 and xParcial <= 7:
                return True
        return False

    def lim(self, coordI, coordParcial):
        if coordParcial < coordI: return 0
        return 7 

    def colisaoPeao(self, time, coordPiece):
        xi = coordPiece[0]
        yi = coordPiece[1]
        if(time == 0): inversor = 1
        else: inversor = -1

        ##Array com possibilidades de movimento após checagem de colisão
        coordPossibles = []

        #Se time branco tenta movimentar para cima
        #Se não para baixo
        yParcial = yi + (1 *inversor)
        
        for i in [-1,0,1]:
            xParcial = xi + i
            if self.checkLims(xParcial, yParcial):
                timePeca = self.tabuleiro.getPieceTime((xParcial, yParcial))
                if(i == 0):
                    if(timePeca == None): coordPossibles.append((xParcial, yParcial))
                else:
                    if(timePeca == (not time)): coordPossibles.append((xParcial, yParcial))
        
        if((time == 0 and yi == 1) or (time == 1 and yi == 6)):
            yParcial = yi + (2 *inversor)
            xParcial = xi
            timePeca = self.tabuleiro.getPieceTime((xParcial, yParcial))
            if(timePeca == None): coordPossibles.append((xParcial, yParcial))

        #Depois implemnentar captura en passant
        return coordPossibles

    def descobrePecaMov(self, time, destino, captura, coordAmb):

        coordPossiblePieces = []

        if(time == 0): inversor = 1; rankExcept = 1
        else: inversor = -1; rankExcept = 6

        #Apenas movimentos verticais
        xParcial = destino[0]
        for i in [1,2]:
            yParcial = destino[1] - i * inversor
            if(i == 2 and yParcial != rankExcept): break
            if(self.checkLims(xParcial, yParcial)):
                piece = self.tabuleiro.get_pedra_by_pos((xParcial, yParcial))
                typePiece = self.tabuleiro.checkTypePiece(piece, 'peao')
                if(typePiece == True and piece.time == time):
                    pieceDestinoTime =  self.tabuleiro.getPieceTime(destino)
                    if(pieceDestinoTime == None): coordPossiblePieces.append((xParcial, yParcial))

        #Se houve capturas o peão veio das colunas ao lado
        if (captura == 'x'):
            for i in [1,2]:
                xParcial = destino[0] + pow(-1,i)
                yParcial = destino[1] - 1 * inversor
                if(self.checkLims(xParcial, yParcial)):
                    piece = self.tabuleiro.get_pedra_by_pos((xParcial, yParcial))
                    typePiece = self.tabuleiro.checkTypePiece(piece, 'peao')
                    if(typePiece == True and piece.time == time):
                        pieceDestinoTime =  self.tabuleiro.getPieceTime(destino)
                        if(pieceDestinoTime == (not time)): coordPossiblePieces.append((xParcial, yParcial))

        ##Array com coords das células com peças (das coordPossibles) #ver peças são não vazias e do tipo correto e conta
        coordPieces = []
        count = 0 #conta quantas peças foram encontradas
        for c in coordPossiblePieces:
            piece = self.tabuleiro.get_pedra_by_pos(c)
            if (piece != None):
                if(self.tabuleiro.checkTypePiece(piece, 'peao')):
                    count += 1
                    coordPieces.append(c)

        coordPiece: tuple #coordenada da peça referida pelo movimento
        newCoordPieces = coordPieces.copy()
        if(count == 0): return {'status': False, 
                                'msg': 'Esse movimento não pode ser realizado por nenhuma peça do seu time'}
        if(count == 1): coordPiece = newCoordPieces[0]
        if(count > 1):
            if(coordAmb != (None, None)): 
                if(coordAmb[0] != None):[newCoordPieces.remove(c) for c in coordPieces if coordAmb[0] != c[0]]
                if(coordAmb[1] != None):[newCoordPieces.remove(c) for c in coordPieces if coordAmb[1] != c[1]]
            else:
                return {'status': False, 
                        'msg': "O movimento é ambíguo, especifique a peça referida"}
            if(len(newCoordPieces) == 1): coordPiece = newCoordPieces[0]
            else: return {'status': False, 
                        'msg': "Reveja a sua string de desambiguação."}
        

        return {'status': True, 'coordPiece': coordPiece}

    def executeMovement(self, coordPiece, destino, coordPossibles, captura):
        
        #Verifica se movimento feito está no range calculado pela máquina
        for c in coordPossibles:
            if(c == destino): 
                if(captura == 'x'): self.tabuleiro.capturaPedra(coordPiece, destino)
                else: self.tabuleiro.movePedra(coordPiece, destino)
                return {'status': True}

        return {'status': False, "msg": "Esse movimento não é possível"}
        

    def checaMovimentoTorre(time, matches):
        pass

    def checaMovimentoCavalo(time, matches):
        pass

    def checaMovimentoBispo(time, matches):
        pass

    def checaMovimentoRainha(time, matches):
        pass

    def checaMovimentoRei(time, matches):
        pass

    def  verifyMovement(self, time, letraPeca, destino, captura, coordAmb):
        
        if(letraPeca == None): #peão
            retorno = self.descobrePecaMov(time, destino, captura, coordAmb)
            if(retorno['status']):
                coordPiece = retorno['coordPiece']
                coordPossibles = self.colisaoPeao(time, coordPiece)
            else: return retorno
        elif (letraPeca == 'T'): #Torre
            pass
        elif(letraPeca == 'N'): #Knight
            pass
        elif(letraPeca == 'B'): #Bishop
            pass
        elif(letraPeca == 'Q'): #Queen
            pass
        elif(letraPeca == 'K'): #King
            pass


        retorno = self.executeMovement(coordPiece, destino, coordPossibles, captura)
        return retorno


    def formatCoordsToHumans(self, coord: tuple):
        col = str(chr(int(coord[0]) + ord('a')))
        lin = str(int(coord[1]) + 1)
        return (col + lin)

    def formatCoordsToMachine(self, col: chr, lin: chr):
        if(col != None): c = ord(col) - ord('a')
        else: c = None
        if(lin != None): l = int(lin) - 1
        else: l = None
        return (c, l)

    def formatMatches(self, matches):
        formatted_matches = {}
        
        peca = matches['letraPeca']
        ambiguo = matches['amb']
        colunaAmb = matches['colunaAmb']
        linhaAmb = matches['linhaAmb']
        captura = matches['captura']
        destinoColuna = matches['destinoColuna']
        destinoLinha = matches['destinoLinha']
        prom = matches['prom']
        check = matches['check']
        checkMate = matches['checkmate']

        destino = self.formatCoordsToMachine(destinoColuna, destinoLinha)
        coordAmb = self.formatCoordsToMachine(colunaAmb, linhaAmb)

        ##
        formatted_matches = {'peca': matches['letraPeca'],
                            'destino': destino,
                            'captura': matches['captura'],
                            'coordAmb': coordAmb
                            }

        return formatted_matches

    
    def checaMovimento(self, time: bool(), cadeia: str()):
        match = re.fullmatch(r"(?P<letraPeca>[KQRBN])?(?P<amb>(?P<colunaAmb>[a-h])?(?P<linhaAmb>[1-8])?)?(?P<captura>x)?(?P<destino>(?P<destinoColuna>[a-h])(?P<destinoLinha>[1-8]))(?P<prom>(?(letraPeca)|[QRBN]))?((?P<check>\+)?|(?P<checkmate>#))", cadeia)
        #Se deu match verifica se o movimento é legal
        if(match):
            matches = match.groupdict()
            formatted_matches = self.formatMatches(matches)
            retorno = self.verifyMovement(time, 
                                          formatted_matches['peca'], 
                                          formatted_matches['destino'], 
                                          formatted_matches['captura'], 
                                          formatted_matches['coordAmb'])
            
            return retorno
        else:
            return {'status': False, 'msg': 'Seu movimento está formado incorretamente.'}



##Contruir um catálogo de erros