
#include <stdio.h>
#include <stdlib.h>
 
#include <arpa/inet.h>
#include <sys/socket.h>
 
int main( int argc , char ** argv ) {
	struct sockaddr_in saddr, caddr;
 
	char buf[100] ;
	char str[100] ;
 
	int listenfd, connfd;
	int addr_len;
 
	listenfd = socket( AF_INET, SOCK_STREAM, 0 );
 
	memset( &saddr, 0, sizeof(saddr) );
	memset( buf, 0, 100 );
	memset( buf, 0, 100 );
	saddr.sin_family = AF_INET;
	saddr.sin_port = htons( 8001 );
	saddr.sin_addr.s_addr = htonl( INADDR_ANY ); //any address
 
	bind( listenfd, (struct sockaddr *)&saddr, 16 );
 
	listen( listenfd, 20 );
 
	printf( "Accepting connections ... \n" );
 
	int i, n;
	while(1)
	{
		addr_len = sizeof( caddr );
		connfd = accept( listenfd, (struct sockaddr*)&caddr, &addr_len );
 
		//n = read( listenfd, buf, 100 );
		n = recv( connfd, buf, 100, 0  );
		
		printf("Recive from %s : %d \n",  inet_ntop( AF_INET, &caddr.sin_addr, str, sizeof(str) ), ntohs(caddr.sin_port) );
 
		for(i=0; i<n; i++)
		{
			buf[i] = toupper( buf[i] );
		}
 
		//write( connfd, buf, n+1 );
		send( connfd, buf, n+1, 0 );
		
		printf("Send : %s \n", buf);
		close( connfd );
	}
 
	return 0;
}
