//user.cc
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <cstring>
#include <stdlib.h>

#pragma comment(lib, "ws2_32.lib")

#define MAX_LINE 100
#define LINE_ARRAY_SIZE (MAX_LINE+1)

using namespace std;

int main()
{
  WSADATA wsaData;
  SOCKET socketDescriptor;
  unsigned short int serverPort;
  struct sockaddr_in serverAddress;
  struct hostent *hostInfo;
  char buf[LINE_ARRAY_SIZE], c;

  // 初始化 Winsock
  if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
    cerr << "WSAStartup failed\n";
    exit(1);
  }

  cout << "Enter server host name or IP address: ";
  cin.get(buf, MAX_LINE, '\n');

  // gethostbyname() 获取主机信息
  hostInfo = gethostbyname(buf);
  if (hostInfo == NULL) {
    cout << "problem interpreting host: " << buf << "\n";
    WSACleanup();
    exit(1);
  }

  cout << "Enter server port number: ";
  cin >> serverPort;
  cin.get(c); // 清除换行符

  // 创建套接字
  socketDescriptor = socket(AF_INET, SOCK_STREAM, 0);
  if (socketDescriptor == INVALID_SOCKET) {
    cerr << "cannot create socket\n";
    WSACleanup();
    exit(1);
  }

  // 连接到服务器
  serverAddress.sin_family = hostInfo->h_addrtype;
  memcpy((char *) &serverAddress.sin_addr.s_addr,
         hostInfo->h_addr_list[0], hostInfo->h_length);
  serverAddress.sin_port = htons(serverPort);
				
  if (connect(socketDescriptor,
              (struct sockaddr *) &serverAddress,
              sizeof(serverAddress)) == SOCKET_ERROR) {
    cerr << "cannot connect\n";
    closesocket(socketDescriptor);
    WSACleanup();
    exit(1);
  }

  cout << "\nEnter some lines, and the server will modify them and\n";
  cout << "send them back.  When you are done, enter a line with\n";
  cout << "just a dot, and nothing else.\n";
  cout << "If a line is more than " << MAX_LINE << " characters, then\n";
  cout << "only the first " << MAX_LINE << " characters will be used.\n\n";

  // 提示用户输入
  cout << "Input: ";
  cin.get(buf, MAX_LINE, '\n');
  while (cin.get(c) && c != '\n') 
    ; // 消耗剩余字符

  // 当用户输入单独的点时停止
  while (strcmp(buf, ".")) {
    // 发送数据到服务器
    if (send(socketDescriptor, buf, strlen(buf) + 1, 0) == SOCKET_ERROR) {
      cerr << "cannot send data ";
      closesocket(socketDescriptor);
      WSACleanup();
      exit(1);
    }

    // 清空缓冲区
    memset(buf, 0x0, LINE_ARRAY_SIZE);

    // 从服务器读取修改后的数据
    if (recv(socketDescriptor, buf, MAX_LINE, 0) == SOCKET_ERROR) {
      cerr << "didn't get response from server?";
      closesocket(socketDescriptor);
      WSACleanup();
      exit(1);
    }

    cout << "Modified: " << buf << "\n";

    // 再次提示用户输入
    cout << "Input: ";
    cin.get(buf, MAX_LINE, '\n');
    while (cin.get(c) && c != '\n')
      ; // 消耗剩余字符
  }

  closesocket(socketDescriptor);
  WSACleanup();
  return 0;
}
