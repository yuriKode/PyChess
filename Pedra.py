class Pedra:

    def __init__(self, time: bool, pos: tuple, img: list =  None, lamb_func: str = None ):
        self.time = time  # 0 => branco , 1 => preto
        self.pos = pos  # x => horizontal, y => vertical (limites de 0 a 7)
        self.lamb_func = lamb_func #função de movimento da peça
        self.img = img # string contendo img da peça

class Peao(Pedra):

    ##img = ' () \n(__)'
    def __init__(self, time, pos, img = ['\u2659', '\u265F'] , lamb_func = None):
        super().__init__(time, pos, img, lamb_func)

class Torre(Pedra):

    def __init__(self, time, pos, img = ['\u2656', '\u265C'], lamb_func = None ):
        super().__init__(time, pos, img, lamb_func)

class Cavalo(Pedra):

    def __init__(self, time, pos, img = ['\u2658', '\u265E'], lamb_func = None ):
        super().__init__(time, pos, img, lamb_func)

class Bispo(Pedra):
    
    def __init__(self, time, pos, img = ['\u2657', '\u265D'], lamb_func = None ):
        super().__init__(time, pos, img, lamb_func)

class Rainha(Pedra):

    def __init__(self, time, pos, img = ['\u2655', '\u265B'], lamb_func = None ):
        super().__init__(time, pos, img, lamb_func)

class Rei(Pedra):

    def __init__(self, time, pos, img = ['\u2654', '\u265A'], lamb_func = None ):
        super().__init__(time, pos, img, lamb_func)