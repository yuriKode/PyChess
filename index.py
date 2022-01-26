### CHESS just to practice

from Xadrez import Xadrez       
 
##Início - Cria instância do xadrez
jogo = Xadrez()

jogo.cria_jogo() ## jogo padrao
jogo.ver()

entrada = str()
msg: str()
time = 0 # 0 - Representa time branco, 1 - time preto
while(1):
    if(not time): msg = "Time Branco, sua vez: "
    else: msg = "Time Preto, sua vez: "

    entrada = input(msg) # Ler input do jogador
    if(entrada == 'quit'): break
    mov = jogo.checaMovimento(time, entrada)
    if(mov):
        print(mov)
        if(mov[0] == False):
            continue
        jogo.ver()
    else:
        print('Seu movimento foi inválido, tente novamente')
        continue
    
    time = not time

""" Rotina do jogo
        Jogador = branco (branco começa)
        Vez do jogador: jogador digita movimento
        Avalia se movimento digitado no prompt é válido, 
            Se sim => movimento válido, executa movimento
                Ver se foi checkmate
                    Se sim
                        Termina o jogo
                    Se não
                        Alterna jogador
                        Volta para -> Vez do jogador
            Se não => movimento inválido
                Volta para -> Vez do Jogador 
"""
""" game = True
time = 0
while(game):
    movimento = input("Sua vez: ")
    if(avalia_movimento()):
        pass """


"""
Retornos da função avalia movimento

continua - vai para a próxima jogada
check - avisa que foi check e vai para a próxima jogada
checkmate - termina o jogo, time que fez o movimento ganha
empate - emite mensagem para o outro jogador que houve uma proposta de empate, pergunta se aceita ou não
         se aceitar, termina o jogo
         se não aceitar, continua o jogo



"""


"""
Aqui movi uma torre. Posso testar mais o gráfico.
Posso arrumar melhores as funções.
Ainda preciso estudar sobre classes em Python.
Ainda preciso ler o material sobre xadrez e nomenclatura que separei em algum lugar por aqui.
O próximo passo provalvelmente é printar as linhas e colunas 'a' a 'h' e 0 a 7
Depois começar a construir a lógica de movimento dos peões, movimentos permitidos.
Posso também começar a construir a formatação do input dos jogadores
Também é possível melhorar a classe jogadores (se houver) cadastro e exibição dos nomes na tela.
Importante começar a separar os arquivos e comentar melhor os códigos.
Continuar lendo o material de python
Criar arquivo para guardar histórico das partidas ref: https://docs.python.org/3.8/tutorial/inputoutput.html#reading-and-writing-files
"""


##continuar inserir reis e rainhas, ler artigo do wikipedia sobre xadrez, depois estudar notação
##colocar o nome das colunas e linhas ao lado do campo, de 'a' a 'h' e de 1 a 8

#jogo.ver()
#print(lista)

##printa linha teste
# o campo terá 64x32https://docs.python.org/3.8/tutorial/inputoutput.html#methods-of-file-objects
# cada bloco de posição terá tamanho de 8x4, as bordas fazem parte
# Depois ver o que pode ser melhorado usando as formatações de strings fornecidas por python
# ref: https://docs.python.org/3.8/library/string.html#formatstrings
# ver referência https://docs.python.org/3.8/library/string.html#formatspec
# Depois implementar atualizaçao da tela, sem printar novamente (será isso possível no prompt,
# provavelmente não, usar alguma interface de usuário decente)

## movimento

# Tarefas
# reler os comentários do código
# criar módulos para diminuir tamanho do código na página principal
# terminar de ler material sobre chess notation https://en.wikipedia.org/wiki/Algebraic_notation_(chess)#Castling
# ver como fazer a leitura do input dos movimentos das peças, ver a opções de formatação de string ou regex
# começar a fazer de forma burra e ir aprimorando... estudar função input() python, ver o que se pode fazer
# ver se é necessário primeiro construir as funções de movimento da peça


"""
Estrutura

    A classe principal é Xadrez. Ela conterá atributos de 2 tipos:
        tabuleiro: Tabuleiro.
        jogadores: list <Jogador>. (lista de jogadores)
        # Em geral haverá apenas 1 tabuleiro e 2 jogadores
    
    A classe Tabuleiro atributos dos seguintes tipos:
        campo: list<list<list<Pedra>>> (matriz com possíveis posições do tabuleiro)
    
    A classe Jogador posuirá os seguintes atributos:
        nome: str
        adv: str (adversário)



"""