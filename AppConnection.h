#pragma once

#include <winsock2.h>
#include <ws2tcpip.h>
#include <string>
#include <optional>

// Link Winsock library
#pragma comment(lib, "ws2_32.lib")

// TCP Client structure
struct TCPClient {
    SOCKET sock;
    sockaddr_in serverAddr;
};

// TCP Server structure
struct TCPServer {
    SOCKET listenSock;
    SOCKET clientSock;
    sockaddr_in serverAddr;
    sockaddr_in clientAddr;
};

// Client functions
std::optional<TCPClient> setupClient(const std::string& ip, int port);
void sendMessage(const TCPClient& client, const std::string& msg);
std::string receive(const TCPClient& client);

// Server functions
std::optional<TCPServer> setupServer(int port);
void sendMessage(const TCPServer& server, const std::string& msg);
std::string receive(const TCPServer& server);