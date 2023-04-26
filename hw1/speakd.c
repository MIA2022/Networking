/**
 ** speakd.c  -  a server program that uses the socket interface to tcp
 **
 **/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include "speakd.h"

/*
 convert www.baidu.com to ip address(IP address translation)
 */
extern char *inet_ntoa( struct in_addr );

#define NAMESIZE		255
#define BUFSIZE			81
#define listening_depth		2

void error(const char *msg){
    perror(msg);
    exit(1);
}

void speakd( int server_number )
{
int			c, i;
int			n, len;
short			fd, client_fd;
struct sockaddr_in	address, client;
struct hostent		*node_ptr;
char			local_node[NAMESIZE];
char			buffer[BUFSIZE+1];
char            subbuff[255];
/*  get the internet name of the local host node on which we are running  */
if( gethostname( local_node, NAMESIZE ) < 0 )
	{
	perror( "server gethostname" );
	exit(1);
	}
fprintf(stderr, "server running on node %s\n", local_node);

/*  get structure for local host node on which server resides  */
if( (node_ptr = gethostbyname( local_node )) == NULL )
	{
	perror( "server gethostbyname" );
	exit(1);
	}

/*  set up Internet address structure for the server  */
memset(&address, 0, sizeof(address));
address.sin_family = AF_INET;
memcpy(&address.sin_addr, node_ptr->h_addr, node_ptr->h_length);
address.sin_port = htons(server_number);

fprintf(stderr, "server full name of server node %s, internet address %s\n",
		node_ptr->h_name, inet_ntoa(address.sin_addr));

/*  open an Internet tcp socket  */
if( (fd = socket(AF_INET, SOCK_STREAM, 0)) < 0 )
	{
	perror( "server socket" );
	exit(1);
	}

/*  bind this socket to the server's Internet address  */
if( bind( fd, (struct sockaddr *)&address, sizeof(address) ) < 0 )
	{
	perror( "server bind" );
	exit(1);
	}

/*  now find out what local port number was assigned to this server  */
len = sizeof(address);
if( getsockname( fd, (struct sockaddr *)&address, &len ) < 0 )
	{
	perror( "server getsockname" );
	exit(1);
	}

/*  we are now successfully established as a server  */
fprintf(stderr, "server at internet address %s, port %d\n",
		inet_ntoa(address.sin_addr), ntohs(address.sin_port));

/*  start listening for connect requests from clients  */
if( listen( fd, listening_depth ) < 0 )
	{
	perror( "server listen" );
	exit(1);
	}

/*  now accept a client connection (we'll block until one arrives)  */
len = sizeof(client);
if( (client_fd = accept(fd, (struct sockaddr *)&client, &len)) < 0 )
	{
	perror( "server accept" );
	exit(1);
	}

/*  we are now successfully connected to a remote client  */
fprintf(stderr, "server connected to client at Internet address %s, port %d\n",
		inet_ntoa(client.sin_addr), ntohs(client.sin_port));

    n=write(client_fd,"Me:\n", strlen("Me:"));
    
S:  memset(buffer, 0, BUFSIZE);
    memset(subbuff, 0, BUFSIZE);
    n= read(client_fd, buffer, BUFSIZE);
    
    if (n<0){
        perror( "Error on reading" );
    }else{
        // Server send message back as a reply to client.
        n= write(client_fd,"(Server received message.)\nx\n", strlen("(Server received message.)\nx\n"));
        //Client input a “xx” on a line by itself and terminate chat.
        if(strlen(buffer)>=3&&buffer[strlen(buffer)-2]=='x'&&buffer[strlen(buffer)-3]=='x'){
            memcpy(subbuff, buffer, strlen(buffer)-3);
            printf("\nClient:\n%s\n\nReminder: Client Exit...Chat is over. The connection is terminated.\n", subbuff);
            goto Q;
        }// Client input a “x” on a line by itself. Client finished with writing and the writing control is shifted to server.
        else{
            printf("\nClient:\n%s\nMe:\n", buffer);
        }
        
        memset(buffer, 0, BUFSIZE);
        
        int c, i=0;
        while((c = getchar()) != EOF&&i<BUFSIZE){
            buffer[i]=c;
            //Server input a “xx” on a line by itself and terminate chat.
            if(i>2&&buffer[i-3]=='\n'&&buffer[i-2]=='x'&&buffer[i-1]=='x'&&c=='\n'||i==2&&buffer[i-2]=='x'&&buffer[i-1]=='x'&&c == '\n'){
                n=write(client_fd, buffer, strlen(buffer));
                printf("\nReminder: You have selected to exit...Chat is over. The connection is terminated.\n");
                goto Q;
            }// Server input a “x” on a line by itself. Server finished with writing and the writing control is shifted to server.
            else if(i>1&&buffer[i-2]=='\n'&&buffer[i-1]=='x'&&c == '\n'){
                n=write(client_fd, buffer, strlen(buffer)-2);
                if(n<0)
                    perror("Error on writing");
                goto S;
            }else if(i==1&&buffer[i-1]=='x'&&c == '\n'){
                n=write(client_fd, "\n", strlen("\n"));
                if(n<0)
                    perror("Error on writing");
                goto S;
            }
            i++;
        }
    }
    
    
    
    /*  close the connection to the client  */
Q:   if( close(client_fd) < 0 )
        {
        perror( "server close connection to client" );
        exit(1);
        }
//    char* msg= "\nReminder: Server exit...Chat is over. The connection should be terminated.\n";
//    n=write(client_fd, msg, strlen(msg));
    close(client_fd);

    /*  close the "listening post" socket by which server made connections  */
    if( close(fd) < 0 )
        {
        perror( "server close" );
        exit(1);
        }
//    printf("\nReminder: You have selected to exit...Chat is over. The connection is terminated.\n");
    close(fd);
}

