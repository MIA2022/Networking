import pygame  # Imports the pygame library for creating a graphical interface
from network2 import Network  # Imports the Network class from the network module.
from board import Board
from button import Button

pygame.font.init()  # Initializes the pygame font module.

width = 700  # Sets the window width to 700 pixels.
height = 700  # Sets the window height to 700 pixels.
win = pygame.display.set_mode((width, height))  # Creates a window with the specified width and height.
pygame.display.set_caption("Tic Tac Toe")  # Sets the window title to "Client"


def draw_message(message, font_size, font_color, background_color=None, text_x=None, text_y=None):
    font = pygame.font.SysFont("comicsans", font_size)
    text = font.render(message, True, font_color, background_color)
    if text_x is None:
        text_x = width / 2 - text.get_width() / 2
    # Use the provided text_y value if given, otherwise calculate it
    if text_y is None:
        text_y = height / 2 - text.get_height() / 2
    win.blit(text, (text_x, text_y))


# redrawing the game window. displaying game information and buttons on the screen,
# depending on the current game state.
# updating the display based on the current game state,
def redrawWindow(win, game, player):
    win.fill((240, 240, 240))

    if not (game.connected()):
        draw_message("Waiting for Player...", 75, (64, 224, 208), (255, 127, 80))
    elif game.choices != ['agree', 'agree']:
        clear_gameboard(gameboard)
        choiceExitBtn.draw(win)
        if player == 0:
            draw_message("You play first and be 'X' player!", 35, (255, 0, 0), None, None, 240)
        else:
            draw_message("You play second and be 'O' player!", 35, (255, 0, 0), None, None, 240)
        agreeBtn.draw(win)
        disagreeBtn.draw(win)
        draw_message("(Please make choice!  )", 20, (255, 0, 0), None, None, 300)
        draw_message("(Game start only when click 'Agree'! Or you can click 'Exit' to exit game )", 20, (255, 0, 0),
                     None, None, 350)
    else:
        board.draw(win, gameboard)
        exitBtn.draw(win)
        print("game.game_result", game.game_result)
        if player == 0:
            draw_message("You are 'X' player!", 30, (255, 0, 0), None, None, 35)
        else:
            draw_message("You are 'O' player!", 30, (255, 0, 0), None, None, 35)

        if game.game_result != -1:
            print(game.game_result)
            replayBtn.draw(win)
            draw_message("'Replay' button doesn't work! Game replay automatically", 15, (255, 0, 0), None, None, 15)
            if (game.game_result == 1 and player == 0) or (game.game_result == 2 and player == 1):
                draw_message("You Won!", 90, (255, 0, 0), None, 240)
            elif game.game_result == 0:
                draw_message("Tie Game!", 90, (255, 0, 0), None, 240)
            elif (game.game_result == 1 and player == 1) or (game.game_result == 2 and player == 0):
                draw_message("You Lost...", 90, (255, 0, 0), None, 240)

    pygame.display.update()


board = Board(125, 90, 150)
replayBtn = Button("Replay", 75, 575, (255, 255, 255), (128, 128, 128))
exitBtn = Button("Exit", 275, 575, (255, 255, 255), (178, 34, 34))
agreeBtn = Button("Agree", 50, 500, (34, 139, 34), (255, 182, 193))
disagreeBtn = Button("Disagree", 250, 500, (65, 105, 225), (255, 215, 0))
choiceExitBtn = Button("Exit", 450, 500, (231, 84, 128), (255, 255, 255))
gameboard = [" " for _ in range(9)]


def clear_gameboard(gameboard):
    for i in range(len(gameboard)):
        gameboard[i] = " "
    return gameboard


def check_valid_move(gameboard, position):
    return gameboard[position] == " "


def match_board(position):
    if position == "7":
        return 0
    elif position == "8":
        return 1
    elif position == "9":
        return 2
    elif position == "4":
        return 3
    elif position == "5":
        return 4
    elif position == "6":
        return 5
    elif position == "1":
        return 6
    elif position == "2":
        return 7
    elif position == "3":
        return 8
    elif position == 0:
        return "7"
    elif position == 1:
        return "8"
    elif position == 2:
        return "9"
    elif position == 3:
        return "4"
    elif position == 4:
        return "5"
    elif position == 5:
        return "6"
    elif position == 6:
        return "1"
    elif position == 7:
        return "2"
    elif position == 8:
        return "3"


# handling game events, such as button clicks and receiving updates from the server.
#  handle game logic and state changes.
def main():
    run = True
    n = Network()
    # print("IP Address", n.getIP)
    player = int(n.getP())
    print("You are player", player)

    while run:

        try:
            game = n.send("get")
        except Exception as e:
            print(f"An exception occurred: {e}")
            run = False
            print("Couldn't get game")
            break
        try:

            for element in game.move1:
                print(match_board(element))
                gameboard[match_board(element)] = "X"
            for element in game.move2:
                print(match_board(element))
                gameboard[match_board(element)] = "O"

        except Exception as e:
            print(f"An exception occurred: {e}")
            break

        if game.exit:
            win.fill((240, 240, 240))
            draw_message("Someone Exit. Game Stop...", 50, (255, 0, 0))
            pygame.display.update()
            pygame.time.delay(4000)
            run = False
            pygame.quit()
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_position = board.click(pos)
                if (clicked_position in range(9)) and game.connected() and game.choices == ['agree', 'agree']:
                    if player == 1:
                        if check_valid_move(gameboard, clicked_position) and game.p1Went[game.round] and not \
                                game.p2Went[game.round]:
                            n.send(match_board(clicked_position))
                    elif player == 0:
                        if check_valid_move(gameboard, clicked_position) and not game.p2Went[game.round] and not \
                                game.p1Went[game.round]:
                            n.send(match_board(clicked_position))
                elif agreeBtn.click(pos) and game.connected() and game.choices != ['agree', 'agree']:
                    n.send("agree")
                elif disagreeBtn.click(pos) and game.connected() and game.choices != ['agree', 'agree']:
                    n.send("disagree")
                elif choiceExitBtn.click(pos) and game.connected() and game.choices != ['agree', 'agree']:
                    n.send('exit')
                elif exitBtn.click(pos) and game.connected() and game.choices == ['agree', 'agree']:
                    n.send('exit')
        redrawWindow(win, game, player)


# handling menu events, such as starting the game and quitting the application.
def start_client():
    def menu_screen():
        run = True

        while run:
            win.fill((240, 240, 240))
            draw_message("Click to Play!", 80, (231, 84, 128), None, 150, 200)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        main()

    # ensures that the menu screen is displayed again after the game ends.
    while True:
        menu_screen()


start_client()
