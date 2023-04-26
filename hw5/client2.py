import pygame
from network2 import Network
import pickle
pygame.font.init()

width = 800
height = 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color,tag):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 150
        self.tag = tag

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
        



def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()) or game.choices != ['agree', 'agree']:
    # if not(game.connected()):
        print("game.choices", game.choices)
        print("game.choices != ['agree', 'agree']", game.choices != ['agree', 'agree'])
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:

        font = pygame.font.SysFont("comicsans", 60)
        text1 = font.render("Your turn", 1, (0, 255, 255))
        text2 = font.render("Waiting...", 1, (0, 255, 255))

        if (p == 0 and not game.p1Went[game.round] )or (p ==1 and game.p1Went[game.round]):
            win.blit(text1, (240, 100))
        else:
            win.blit(text2, (240, 100))

        for btn in btns:
            btn.text = ""
        for p1move in game.move1:
            btns[int(p1move)-1].text = "X"
        for p2move in game.move2:
            btns[int(p2move)-1].text = "O"
        
        for btn in btns:
            btn.draw(win)

  

    pygame.display.update()


btns = [Button("",90,660,(255,255,255),"1"),Button("",310,660,(255,255,255),"2"),Button("",530,660,(255,255,255),"3"),Button("",90,470,(255,255,255),"4"),Button("",310,470,(255,255,255),"5"),Button("",530,470,(255,255,255),"6"),Button("", 90, 280, (255,255,255),"7"), Button("", 310, 280, (255,255,255),"8"), Button("", 530, 280, (255,255,255),"9")]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)


    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        redrawWindow(win, game, player)

        if game.winner() !=-1:
            print()
            pygame.time.delay(500)
            try:
                font = pygame.font.SysFont("comicsans", 90)
                if (game.winner() == 1 and player == 0) or (game.winner() == 2 and player == 1):
                    text = font.render("You Won!", 1, (255,0,0))
                elif game.winner() == 0:
                    text = font.render("Tie Game!", 1, (255,0,0))
                elif (game.winner() == 1 and player ==1) or (game.winner()==2 and player == 0):
                    text = font.render("You Lost...", 1, (255, 0, 0))

                win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(4000)
                game = n.send("reset")
                
            except:
                run = False
                
                break
            
            
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went[game.round]:
                                n.send(btn.tag)
                        else:
                            if not game.p2Went[game.round] and game.p1Went[game.round]:
                                n.send(btn.tag)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
