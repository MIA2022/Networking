import socket
from _thread import *
import pickle
from game2 import Game

server = socket.gethostname()
port = 5131

server_ip = socket.gethostbyname(server)
print("ipaddress", server_ip)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        # game.make_reset(p)
                        game.resetWent()
                    elif data == "agree" or data == "disagree":
                        game.make_choice(p, data)
                    elif data == "exit":
                        game.exit_game()
                    elif data != "get":
                        if data not in game.move1 and data not in game.move2:
                            if int(p)== 0:
                                if not game.p2Went[game.round] and not game.p1Went[game.round]:
                                    game.play(0,data)
                            else:
                                if game.p1Went[game.round] and not game.p2Went[game.round]:
                                    game.play(1,data)
                    game.winner()
                

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))