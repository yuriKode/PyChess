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

    def fazMovimento(self, partida, chegada):
        self.tabuleiro.movePedra(partida, chegada)
        return True

    
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

        return coordPossibles

    def descobrePecaMov(self, chegada, captura, time):

        coordPossiblePieces = []

        if(time == 0): 
            inversor = 1
            rankExcept = 1
        else: 
            inversor = -1
            rankExcept = 6

        #Apenas movimentos verticais
        xParcial = chegada[0]
        for i in [1,2]:
            yParcial = chegada[1] - i * inversor
            if(i == 2):
                if(yParcial != rankExcept): break
            if(self.checkLims(xParcial, yParcial)):
                piece = self.tabuleiro.get_pedra_by_pos((xParcial, yParcial))
                typePiece = self.tabuleiro.checkTypePiece(piece, 'peao')
                if(typePiece == True and piece.time == time): coordPossiblePieces.append((xParcial, yParcial))

        #Se houve capturas o peão veio das colunas ao lado
        if (captura == 'x'):
            for i in [1,2]:
                xParcial = chegada[0] + pow(-1,i)
                yParcial = chegada[1] - 1 * inversor

                if(self.checkLims(xParcial, yParcial)):
                    piece = self.tabuleiro.get_pedra_by_pos(xParcial, yParcial)
                    typePiece = self.tabuleiro.checkTypePiece(piece, 'peao')
                    if(typePiece == True and piece.time == time): coordPossiblePieces.append((xParcial, yParcial))

        #Depois implemnentar en passant ## Ver Captura

        return coordPossiblePieces

    def checaMovimentoPeao(self, time, formatted_matches):
        #Essa lógica funciona para para o movimento pelo terminal
        #Vamos restringir o número de peças capaz de realizar tal movimento
       
        #yPossibles e xPossibles representam os possíveis pontos de saída da peça
        peca = formatted_matches['peca']
        
        linha = formatted_matches['destinoLinha']
        coluna = formatted_matches['destinoColuna']
        chegada = (coluna, linha)
        captura = formatted_matches['captura']
        amb = formatted_matches['amb']
        colunaAmb = formatted_matches['colunaAmb']
        linhaAmb = formatted_matches['linhaAmb']

        
        ##Coordenada com possíveis peões que pode realizar o movimento desejado
        coordPossiblePieces = self.descobrePecaMov(chegada, captura, time)


        ##Array com coords das células com peças (das coordPossibles)
        coordPieces = []
        count = 0 #conta quantas peças foram encontradas
        for c in coordPossiblePieces:
            piece = self.tabuleiro.get_pedra_by_pos(c)
            if (piece != None):
                if(self.tabuleiro.checkTypePiece(piece, 'peao')):
                    count += 1
                    coordPieces.append(c)

        coordPiece: tuple #coordenada da peça referida pelo movimento
        if(count == 0): return [False, 'Esse movimento não pode ser realizado por nenhuma peça do seu time']
        if(count == 1): coordPiece = coordPieces[0]
        if(count > 1):
            if(amb != None): 
                if(colunaAmb != None):[coordPieces.remove(c) for c in coordPieces if colunaAmb != c[0]]
                if(linhaAmb != None):[coordPieces.remove(c) for c in coordPieces if linhaAmb != c[1]]
            else:
                return [False, "O movimento é ambíguo, especifique a peça referida"]
            coordPiece = coordPieces[0]

        ##Essa parte de cima precisa ser testada
        coordCalculadas = self.colisaoPeao(time, coordPiece)
        
        #Verifica se movimento feito está no range calculado pela máquina
        for c in coordCalculadas:
            if(c == chegada): 
                self.fazMovimento(coordPiece, chegada)
                break

        coordCalculadasToHumans = [self.formatCoordsToHumans(c) for c in coordCalculadas]
        ## AGORA FAZER INTERSEÇÃO DE MOVIMENTO REQUERIDO PELO JOGADOR
        ## versus os movimentos possíveis calculador

        msg1 = "Peças que jogador quer que realize o movimento: " + self.formatCoordsToHumans(coordPiece)
        msg2 = "Possíveis movimento da peça: "
        for c in coordCalculadasToHumans: msg2 += c + " "
        return (True, msg1, msg2)
        

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

    def formatCoordsToHumans(self, coord: tuple):
        col = str(chr(int(coord[0]) + ord('a')))
        lin = str(int(coord[1]) + 1)
        return (col + lin)

    def formatCoordsToMachine(self, col: chr, lin: chr):
        pass

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

        #formata linhas e colunas
        coluna_t = ord(matches['destinoColuna']) - ord('a')
        linha_t = int(matches['destinoLinha']) - 1

        #Se houverem matches nessas posições, formata-as
        if(matches['colunaAmb'] != None): colunaAmb = ord(matches['colunaAmb']) - ord('a')
        if(matches['linhaAmb'] != None): linhaAmb = int(matches['linhaAmb']) - 1

        ##
        formatted_matches = {'peca': matches['letraPeca'],
                        'destinoColuna': coluna_t,
                        'destinoLinha': linha_t,
                        'captura': matches['captura'],
                        'amb': matches['amb'],
                        'colunaAmb': colunaAmb,
                        'linhaAmb': linhaAmb}

        return formatted_matches

    
    def checaMovimento(self, time: bool(), cadeia: str()):
        match = re.fullmatch(r"(?P<letraPeca>[KQRBN])?(?P<amb>(?P<colunaAmb>[a-h])?(?P<linhaAmb>[1-8])?)?(?P<captura>x)?(?P<destino>(?P<destinoColuna>[a-h])(?P<destinoLinha>[1-8]))(?P<prom>(?(letraPeca)|[QRBN]))?((?P<check>\+)?|(?P<checkmate>#))", cadeia)
        #Se deu match verifica se o movimento é legal
        if(match):
            matches = match.groupdict()
            formatted_matches = self.formatMatches(matches)
            peca = formatted_matches['peca']
            
            if(peca == None): #A peça sendo movimentada é peão
                retorno = self.checaMovimentoPeao(time, formatted_matches)

    
            
            return retorno
        else:
            return False



##Contruir um catálogo de erros