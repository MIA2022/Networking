How to run the program?
1. input './speakd' to connect server;
2. input './speak port number' to connect client

The detailed features of the program:

1. The server is started up waiting for a client and the client gets to write first.

    When user input './speakd' and './speak port number', there will be a prompt message 'Please enter message!' from server in Client side.
    At the same time, it will show 'Me:' in client side, client should input the message.

2. The two programs alternate writing, with the current writer getting to write until control is relinquished.

   If client inputs a “x” on a line by itself, the message will be sent to server. In the server side, it will show 'Client: ' as the sign of the message
   from client. The specific message from client will be shown after 'Client: '. “x” will not be shown.  
   At the same time, it will show 'Me:' in server side, server should input the message.
   If client only inputs a “x” on a line by itself, the message will be an '\n'. That is, in the server side, it will show an empty line.
   When server inputs a “x” on a line by itself, it has the same function.

3. A “xx” on a line by itself by either side means that the chat is over and the connection should be terminated.

    Either client or server inputs a “xx” on a line by itself, chat will be terminated. Both client and server will quit.
    If client inputs firstly, in the client side, it will show "Reminder: You have selected to exit...Chat is over. The connection is terminated."
    In the server side, it will show "Reminder: Client Exit...Chat is over. The connection is terminated."
    If server inputs firstly, in the client side, it will show "Reminder: You have selected to exit...Chat is over. The connection is terminated."
    In the client side, it will show "Reminder: Server Exit...Chat is over. The connection should be terminated.".
   
3. The server must always send something back as a reply to any message received from the client.

    Each time server read message successfully from client, it will send a reply message "(Server received message.)" to client.

Demo

Client:
https://postimg.cc/rzJD7k29

Server:
https://postimg.cc/zHXGqyYF
