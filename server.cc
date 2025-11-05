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

  // 初始化 Winsock
  if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
    cerr << "WSAStartup failed";
    exit(1);
  }

  cout << "Enter port number to listen on (between 1500 and 65000): ";
  cin >> listenPort;

  // 创建监听套接字
  listenSocket = socket(AF_INET, SOCK_STREAM, 0);
  if (listenSocket == INVALID_SOCKET) {
    cerr << "cannot create listen socket";
    WSACleanup();
    exit(1);
  }
  
  // 绑定监听套接字到端口
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

  // 开始监听连接
  if (listen(listenSocket, 5) == SOCKET_ERROR) {
    cerr << "listen failed";
    closesocket(listenSocket);
    WSACleanup();
    exit(1);
  }
  
  while (1) {
    cout << "Waiting for TCP connection on port " << listenPort << " ...\n";

    // 接受客户端连接
    clientAddressLength = sizeof(clientAddress);
    connectSocket = accept(listenSocket,
                           (struct sockaddr *) &clientAddress,
                           &clientAddressLength);
    if (connectSocket == INVALID_SOCKET) {
      cerr << "cannot accept connection ";
      continue;
    }
    
    // 显示客户端 IP 地址
    char clientIP[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &clientAddress.sin_addr, clientIP, INET_ADDRSTRLEN);
    cout << "  connected to " << clientIP;

    // 显示客户端端口号
    cout << ":" << ntohs(clientAddress.sin_port) << "\n";

    // 从套接字读取数据
    memset(line, 0x0, LINE_ARRAY_SIZE);
    string word="";
    string notANumber="";
    float cost = 0;
    int number=0;
    bool isanum=false;
    
    int recvResult;
    while ((recvResult = recv(connectSocket, line, MAX_MSG, 0)) > 0) {
      cout << "  --  " << line << "\n";

      // 处理接收到的数据
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

      // 发送修改后的数据回客户端
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
