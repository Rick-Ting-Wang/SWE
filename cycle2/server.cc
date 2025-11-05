//tcp-server.cc
// tcp-server that chops up the input 
//You need to put a fullstop at the end (.) so get last word
//For example
//I am on holiday.

#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <cstring>
#include <stdlib.h>
#include <string>

#pragma comment(lib, "ws2_32.lib")

#define MAX_MSG 100
#define LINE_ARRAY_SIZE (MAX_MSG+1)

using namespace std;

// function that checks if the chunk extracted from the order is a number
bool isNumber(string word)
{
    for (int character = 0; character < word.length(); character++){
        if (isdigit(word[character]) == false)
            return false;
    }
    return true;
}

int main()
{
  WSADATA wsaData;
  SOCKET listenSocket, connectSocket;
  int i;
  unsigned short int listenPort;
  int clientAddressLength;
  struct sockaddr_in clientAddress, serverAddress;
  char line[LINE_ARRAY_SIZE];

  // Initialize Winsock
  if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
    cerr << "WSAStartup failed";
    exit(1);
  }

  cout << "Enter port number to listen on (between 1500 and 65000): ";
  cin >> listenPort;

  // Create listen socket
  listenSocket = socket(AF_INET, SOCK_STREAM, 0);
  if (listenSocket == INVALID_SOCKET) {
    cerr << "cannot create listen socket";
    WSACleanup();
    exit(1);
  }
  
  // Bind socket to port
  serverAddress.sin_family = AF_INET;
  serverAddress.sin_addr.s_addr = htonl(INADDR_ANY);
  serverAddress.sin_port = htons(listenPort);
  
  if (bind(listenSocket,
           (struct sockaddr *) &serverAddress,
           sizeof(serverAddress)) == SOCKET_ERROR) {
    cerr << "cannot bind socket";
    closesocket(listenSocket);
    WSACleanup();
    exit(1);
  }

  // Start listening
  if (listen(listenSocket, 5) == SOCKET_ERROR) {
    cerr << "listen failed";
    closesocket(listenSocket);
    WSACleanup();
    exit(1);
  }
  
  while (1) {
    cout << "Waiting for TCP connection on port " << listenPort << " ...\n";

    // Accept client connection
    clientAddressLength = sizeof(clientAddress);
    connectSocket = accept(listenSocket,
                           (struct sockaddr *) &clientAddress,
                           &clientAddressLength);
    if (connectSocket == INVALID_SOCKET) {
      cerr << "cannot accept connection ";
      continue;
    }
    
    // Display client IP address
    char clientIP[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &clientAddress.sin_addr, clientIP, INET_ADDRSTRLEN);
    cout << "  connected to " << clientIP;

    // Display client port
    cout << ":" << ntohs(clientAddress.sin_port) << "\n";

    // Read data from socket
    memset(line, 0x0, LINE_ARRAY_SIZE);
    string word="";
    string notANumber="";
    float cost = 0;
    int number=0;
    bool isanum=false;
    
    int recvResult;
    while ((recvResult = recv(connectSocket, line, MAX_MSG, 0)) > 0) {
      cout << "  --  " << line << "\n";

      for (i = 0; line[i] != '\0'; i++){
        //the user need to end the order with a full stop (.) to get last word/number 
        if ((line[i] != ' ') && (line[i] != '.')) {
          word=word+line[i];
        }
        // Keep adding a character until reach end of word/number
        if ((line[i] == ' ')|| (line[i]=='.')){
          //Call function to check if chunk of characters is a number
          isanum=isNumber(word);
          //if is a number convert string to number
          if (isanum){
            cout<<"its a number"<<endl;
            number = stoi(word);
          }
          else {
            //If not a number          
            notANumber=word;
            cout<<"its not a number"<<endl;
          }
          //Clear word so can add next word/number
          word="";
        }
      }
      sprintf(line,"The cost of the  booking is: %f ", cost);

      if (send(connectSocket, line, strlen(line) + 1, 0) == SOCKET_ERROR)
        cerr << "Error: cannot send modified data";

      memset(line, 0x0, LINE_ARRAY_SIZE);  // set line to all zeroes
    }
    
    if (recvResult == SOCKET_ERROR) {
      cerr << "recv failed: " << WSAGetLastError() << endl;
    }
    
    cout << "Client disconnected\n";
    closesocket(connectSocket);
  }
  
  closesocket(listenSocket);
  WSACleanup();
  return 0;
}
