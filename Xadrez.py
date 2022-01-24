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

    
    def checkLims(self, coord): #Checa se possível coordenada está no bordo se não retorna impossível
        if coord >= 0 and coord <= 7: return True
        else: return False


    def checaMovimentoPeao(self, time, formatted_matches):
        #Vamos restringir o número de peças capaz de realizar tal movimento
       
        #yPossibles e xPossibles representam os possíveis pontos de saída da peça
        peca = formatted_matches['peca']
        coordPossibles = []
        yPossibles = []
        xPossibles = []
        linha = formatted_matches['destinoLinha']
        coluna = formatted_matches['destinoColuna']
        captura = formatted_matches['captura']

        #Primeiro checamos o time 
        if (time == 0) : #Se time branco deve ter vindo de uma célula inferior
            if(self.checkLims(linha - 1)): yPossibles.append(linha - 1)
            if(linha == 3): ## Excessão da pulada de duas casas no início do jogo
                if(self.checkLims(linha - 2)): yPossibles.append(linha - 2)
        else: #Se não superior
            if(self.checkLims(linha + 1)): yPossibles.append(linha + 1)
            if(linha == 4):
                if(self.checkLims(linha + 2)): yPossibles.append(linha + 2)

        if (captura == 'x'): #Se houve capturas o peão veio das colunas ao lado
            if(self.checkLims(coluna - 1)): xPossibles.append(coluna - 1)
            if(self.checkLims(coluna + 1)): xPossibles.append(coluna + 1)
        else: #Se não da mesma coluna
            xPossibles.append(coluna)

        ##Constroí array com todas coordenadas possíveis de partida
        coordPossibles = [ (x,y) for x in xPossibles for y in yPossibles ]
        ##Array com coords das células com peças (das coordPossibles)
        coordPieces = []
        count = 0 #conta quantas peças foram encontradas
        for c in coordPossibles:
            piece = self.tabuleiro.get_pedra_by_pos(c)
            if (piece != None):
                if(self.tabuleiro.checkTypePiece(piece, 'peao')):
                    count += 1
                    coordPieces.append(c)

        if(count == 0): return [False, 'Esse movimento não pode ser realizado por nenhuma peça do seu time']
        if(count == 1):  
            self.fazMovimento(coordPieces[0], (coluna, linha)) 
            return [True, 'Movimento realizado com sucesso']
        if(count > 1): return [True, 'Há mais de uma peça possível para realizar esse movimento'] #checa ambiguidade
        
        ## PAREI NA IMPLEMENTAÇÃO DA CHECAGEM DE AMBIGUIDADE DO PEÃO
        ##E TAMBÉM NÃO FIZ ALGORITMO DE CAPTURA DO PEÃO
        ##USAR A FUNÇÃO DE COLISÃO DO ARQUIVO LÓGICA VALIDA MOV. TXT
        
        
    
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

        ##
        formatted_matches = {'peca': matches['letraPeca'],
                        'destinoColuna': coluna_t,
                        'destinoLinha': linha_t,
                        'captura': matches['captura']
                        }

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