import socket  # Imports the socket library for creating network connections
import pickle  # Imports the pickle library for serializing and deserializing Python objects.


class Network:
    def __init__(self, host, port):
        # Creates a new socket object for the IPv4 address family (AF_INET)
        # using the TCP protocol (SOCK_STREAM) and assigns it to the self.client attribute.
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Defines the server's IP address as a string.
        self.server = host
        # Defines the server's port number.
        self.port = port
        # Creates a tuple containing the server's IP address and port number.
        self.addr = (self.server, self.port)
        #  Calls the connect method and stores the returned value in self.p.
        self.p = self.connect()

    def getP(self):
        return self.p

    # a method to connect the client to the server.
    def connect(self):
        try:
            #  Connects the client to the server using the address tuple self.addr.
            self.client.connect(self.addr)
            # Receives data from the server, decodes it, and returns it.
            return self.client.recv(2048).decode()
        except:
            pass

    # Defines a method to send data to the server
    def send(self, data):
        try:
            # Encodes the data as a string and sends it to the server.
            self.client.send(str.encode(data))
            # Receives data from the server, deserializes it using the pickle library,
            # and returns it.
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)
