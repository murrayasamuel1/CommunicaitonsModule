#include <iostream>
#include "logger.h"
#include "PresentationLayer.h"

// TCP includes
#include "AppConnection.h"

#include <optional>
#include <thread>
#include <string>



static TCPServer server;
static PresentationLayer pl;

void receive_from_GSA() {
    while (true) {
        std::string msg = receive(server);
        if (!msg.empty()) {
            pl.presentation_channel.push(msg);
        }
    }
}

int main() {
    Logger::clear();
    Logger::log("CM setting up server");

    auto maybeServer = setupServer(5001);
    if (!maybeServer) {
        Logger::log("CM failed to setup server");
        return 1;
    }
    Logger::log("Connection established");
    server = *maybeServer;


    std::thread t1(receive_from_GSA);
    std::thread PlRx(&PresentationLayer::rx, &pl);
    std::thread PlTx(&PresentationLayer::rx, &pl);


    // Wait for threads to finish
    PlRx.join();
    PlTx.join();
    t1.join();




    return 0;
}

