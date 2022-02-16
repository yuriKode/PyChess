### CHESS just to practice

from Chess import Chess
 
game = Chess()
game.createGame() ## game padrao
game.see()

msg: str()
team = False # False is white, true is black
while(1):

    if(not team): msg = "White team, your turn: "
    else: msg = "Black team, your turn: "

    stringInput = input(msg)
    if(stringInput == 'quit'): break
    
    answer = game.readMovement(team, stringInput)
    if(answer['status'] == True): game.see()
    else: print(answer['msg']) ; continue
    
    team = not team


##Stopped in this bug "bc3" -> moved the pawn from c2 to c3, I think that that shouldn't happen