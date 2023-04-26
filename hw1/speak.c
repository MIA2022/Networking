/**
 ** speak.c  -  a server program that uses the socket interface to tcp
 **
 **/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include "speak.h"

extern char *inet_ntoa( struct in_addr );

#define NAMESIZE		255
#define BUFSIZE			81

void speak( int server_number, char *server_node )
{
int			length;
int			n, len;
short			fd;
struct sockaddr_in	address;
struct hostent		*node_ptr;
char			local_node[NAMESIZE];
char			buffer[BUFSIZE];
char            subbuff[255];

/*  get the internet name of the local host node on which we are running  */
if( gethostname( local_node, NAMESIZE ) < 0 )
	{
	perror( "client gethostname" );
	exit(1);
	}
fprintf(stderr, "client running on node %s\n", local_node);

/*  get the name of the remote host node on which we hope to find server  */
if( server_node == NULL )
	server_node = local_node;
fprintf(stderr, "client about to connect to server at port number %d on node %s\n",
		server_number, server_node);

/*  get structure for remote host node on which server resides  */
if( (node_ptr = gethostbyname( server_node )) == NULL )
	{
	perror( "client gethostbyname" );
	exit(1);
	}

/*  set up Internet address structure for the server  */
memset(&address, 0, sizeof(address));
address.sin_family = AF_INET;
memcpy(&address.sin_addr, node_ptr->h_addr, node_ptr->h_length);
address.sin_port = htons(server_number);

fprintf(stderr, "client full name of server node %s, internet address %s\n",
		node_ptr->h_name, inet_ntoa(address.sin_addr));

/*  open an Internet tcp socket  */
if( (fd = socket(AF_INET, SOCK_STREAM, 0)) < 0 )
	{
	perror( "client socket" );
	exit(1);
	}

/*  connect this socket to the server's Internet address  */
if( connect( fd, (struct sockaddr *)&address, sizeof(address) ) < 0 )
	{
	perror( "client connect" );
	exit(1);
	}

/*  now find out what local port number was assigned to this client  */
len = sizeof(address);
if( getsockname( fd, (struct sockaddr *)&address, &length ) < 0 )
	{
	perror( "client getsockname" );
	exit(1);
	}

/*  we are now successfully connected to a remote server  */
fprintf(stderr, "client at internet address %s, port %d\n",
		inet_ntoa(address.sin_addr), ntohs(address.sin_port));

/*  transmit data from standard input to server  */
    

   memset(buffer, 0, BUFSIZE);
    //read server string
    n=read(fd, buffer, BUFSIZE);
    if(n<0)
        perror("Error on reading");
    printf("Please enter message!\n\n%s\n", buffer);
    
S:  memset(buffer, 0, BUFSIZE);
    int c, i=0;
    while((c = getchar()) != EOF&&i<BUFSIZE){
        buffer[i]=c;
        // Client input a “xx” on a line by itself and terminate chat.
        if(i>2&&buffer[i-3]=='\n'&&buffer[i-2]=='x'&&buffer[i-1]=='x'&&c=='\n'||i==2&&buffer[i-2]=='x'&&buffer[i-1]=='x'&&c =='\n'){
            n=write(fd, buffer, strlen(buffer));
            if(n<0)
                perror("Error on writing");
            // Get the reply message from the server.
            memset(buffer, 0, BUFSIZE);
            memset(subbuff, 0, BUFSIZE);
            n=read(fd, buffer, BUFSIZE);
            if(strlen(buffer)>=3&&buffer[strlen(buffer)-1]=='\n'&&
                     buffer[strlen(buffer)-2]=='x'&&
                     buffer[strlen(buffer)-3]=='\n'){
                memcpy(subbuff, buffer, strlen(buffer)-2);
                printf("%s", subbuff);
            }
            printf("\nReminder: You have selected to exit...Chat is over. The connection is terminated.\n");
            goto Q;
        }//Client input a “x” on a line by itself. Client finished with writing and the writing control is shifted to server.
        else if(i>1&&buffer[i-2]=='\n'&&buffer[i-1]=='x'&&c == '\n'){
            n=write(fd, buffer, strlen(buffer)-2);
            if(n<0)
                perror("Error on writing");
            break;
        }else if(i==1&&buffer[i-1]=='x'&&c == '\n'){
            n=write(fd, "\n", strlen("\n"));
            if(n<0)
                perror("Error on writing");
            break;
        }
        i++;
    }
    
F:  memset(buffer, 0, BUFSIZE);
    memset(subbuff, 0, BUFSIZE);
    n=read(fd, buffer, BUFSIZE);
    if(n<0)
        perror("Error on reading");
    //Server input a “xx” on a line by itself and terminate chat.
    if(strlen(buffer)>=3&&buffer[strlen(buffer)-2]=='x'&&buffer[strlen(buffer)-3]=='x'){
        memcpy(subbuff, buffer, strlen(buffer)-3);
        printf("\nServer:\n%s\nReminder: Server Exit...Chat is over. The connection should be terminated.\n", subbuff);
        goto Q;
    }//Get the reply message from the server.
    else if(strlen(buffer)>=3&&buffer[strlen(buffer)-1]=='\n'&&
             buffer[strlen(buffer)-2]=='x'&&
             buffer[strlen(buffer)-3]=='\n'){
        memcpy(subbuff, buffer, strlen(buffer)-2);
        printf("%s", subbuff);
        goto F;
    }//Server input a “x” on a line by itself. Server finished with writing and the writing control is shifted to server.
    else{
        printf("\nServer:\n%s\nMe:\n", buffer);
        goto S;
    }
    


/*  close the connection to the server  */
Q:    if( close(fd) < 0 )
        {
        perror( "client close" );
        exit(1);
        }
     close(fd);
     
}


