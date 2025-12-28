#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")
#include "AppConnection.h"
#include "logger.h"

#include <chrono>
#include <thread>

#include <string>
#include <optional>

int main() {
    Logger::log("Hello from GS");

    // Small delay to let the server start
    std::this_thread::sleep_for(std::chrono::milliseconds(500));

    std::optional<TCPClient> maybeClient;
    while (!maybeClient) {
        maybeClient = setupClient("127.0.0.1", 5001);
        if (!maybeClient) {
            std::cout << "Server not ready, retrying in 1 second...\n";
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
    TCPClient& client = *maybeClient;

    // Send messages
    std::vector<std::string> messages = {"message 1", "message 2", "message 3", "message 4", "message 5"};
    while (!messages.empty()) {
        sendMessage(client, messages.front());
        messages.erase(messages.begin());
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }




    return 0;
}