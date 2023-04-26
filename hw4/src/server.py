import socket  # socket for network communication
import traceback
from _thread import *  # handling multiple connections
import pickle  # serializing and deserializing game objects
from game import Game  # Import the Game class from the game module.


def start_server(port):
    server = socket.gethostname()  # Define server IP address and port number.

    print("IP address", socket.gethostbyname(server))


    # Create a socket object s.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))  # bind the socket to the IP address and port.
    except socket.error as e:
        str(e)

    s.listen(2)  # Set the server to listen for two connections.
    # Print a message indicating the server has started
    print("Waiting for a connection, Server Started")

    connected = set()  # Create a set to store connected clients
    games = {}  # Create a dictionary to store active games
    idCount = 0  # Initialize a counter for client IDs

    # handles communication with each client
    def threaded_client(conn, p, gameId):
        global idCount
        # know p=0 or p=1
        conn.send(str.encode(str(p)))

        while True:
            try:

                data = conn.recv(4096 * 2).decode()
                print("data", data)
                # check if game still exits, then get the game object
                # if one of clients disconnect the game, will delete the game object
                if gameId in games:
                    game = games[gameId]
                    if not data:
                        break
                    else:
                        if data == "reset":
                            game.reset_game()
                        elif data == "exit":
                            game.exit_game()
                        elif data == "agree" or data == "disagree":
                            game.make_choice(p, data)
                        elif data == "resetChoices":
                            game.reset_choices()
                        elif data != "get":
                            game.play(p, data)
                        print("game.get_first_player()", game.get_first_player())
                        print("game.choices", game.choices)

                        # pack game object and send to client
                        conn.sendall(pickle.dumps(game))
                else:
                    break
            except Exception as e:
                print("An exception occurred:", e)
                traceback.print_exc()
                break

        print("Lost connection")
        try:
            del games[gameId]
            print("Closing  Game", gameId)
        except:
            pass
        idCount -= 1  # decrement the global idCount when a client disconnects.
        conn.close()  # Close the connection when the client disconnects

    # waiting for new connections.
    while True:
        conn, addr = s.accept()  # Accept an incoming connection .
        print("Connected to:", addr)  # print the client's IP address

        idCount += 1  # Increment the client ID counter
        p = 0
        # Determine if the connecting client is player 0 or 1, and assign the appropriate game ID.
        gameId = (idCount - 1) // 2
        # games[gameId] = Game(gameId)
        if idCount % 2 == 1:
            # If the client is player 0, create a new game and print a message.
            games[gameId] = Game(gameId)
            print("Creating a new game...")
        else:
            # If the client is player 1, set the game's ready attribute to True
            games[gameId].ready = True
            p = 1

        # Start a new thread for each incoming connection, passing the connection
        # object, player number, and game ID to the threaded_client function.
        start_new_thread(threaded_client, (conn, p, gameId))
