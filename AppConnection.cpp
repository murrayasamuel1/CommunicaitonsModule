#include "AppConnection.h"
#include <iostream>

// --------------------- TCP CLIENT ---------------------
std::optional<TCPClient> setupClient(const std::string& ip, int port) {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2,2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed\n";
        return std::nullopt;
    }

    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        std::cerr << "socket() failed\n";
        WSACleanup();
        return std::nullopt;
    }

    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);

    if (inet_pton(AF_INET, ip.c_str(), &serverAddr.sin_addr) <= 0) {
        std::cerr << "Invalid server IP\n";
        closesocket(sock);
        WSACleanup();
        return std::nullopt;
    }

    if (connect(sock, reinterpret_cast<sockaddr*>(&serverAddr), sizeof(serverAddr)) == SOCKET_ERROR) {
        int err = WSAGetLastError();
        std::cerr << "connect() failed. Error: " << err << "\n";
        closesocket(sock);
        WSACleanup();
        return std::nullopt;
    }

    return TCPClient{sock, serverAddr};
}

void sendMessage(const TCPClient& client, const std::string& msg) {
    send(client.sock, msg.c_str(), static_cast<int>(msg.size()), 0);
}

std::string receive(const TCPClient& client) {
    char buffer[1024];
    int bytesReceived = recv(client.sock, buffer, sizeof(buffer)-1, 0);
    if (bytesReceived <= 0) return {};
    buffer[bytesReceived] = '\0';
    return std::string(buffer);
}

// --------------------- TCP SERVER ---------------------
std::optional<TCPServer> setupServer(int port) {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2,2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed\n";
        return std::nullopt;
    }

    SOCKET listenSock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (listenSock == INVALID_SOCKET) {
        std::cerr << "socket() failed\n";
        WSACleanup();
        return std::nullopt;
    }

    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(listenSock, reinterpret_cast<sockaddr*>(&serverAddr), sizeof(serverAddr)) == SOCKET_ERROR) {
        int err = WSAGetLastError();
        std::cerr << "bind() failed. WSA error: " << err << "\n";
        closesocket(listenSock);
        WSACleanup();
        return std::nullopt;
    }

    if (listen(listenSock, SOMAXCONN) == SOCKET_ERROR) {
        std::cerr << "listen() failed\n";
        closesocket(listenSock);
        WSACleanup();
        return std::nullopt;
    }

    std::cout << "Server listening on port " << port << "\n";

    sockaddr_in clientAddr{};
    int clientLen = sizeof(clientAddr);
    SOCKET clientSock = accept(listenSock, reinterpret_cast<sockaddr*>(&clientAddr), &clientLen);
    if (clientSock == INVALID_SOCKET) {
        std::cerr << "accept() failed\n";
        closesocket(listenSock);
        WSACleanup();
        return std::nullopt;
    }

    return TCPServer{listenSock, clientSock, serverAddr, clientAddr};
}

void sendMessage(const TCPServer& server, const std::string& msg) {
    send(server.clientSock, msg.c_str(), static_cast<int>(msg.size()), 0);
}

std::string receive(const TCPServer& server) {
    char buffer[1024];
    int bytesReceived = recv(server.clientSock, buffer, sizeof(buffer)-1, 0);
    if (bytesReceived <= 0) return {};
    buffer[bytesReceived] = '\0';
    return std::string(buffer);
}