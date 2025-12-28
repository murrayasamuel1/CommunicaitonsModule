//
// Created by murra on 12/21/2025.
//
// logger.cpp
#include "logger.h"

std::mutex Logger::mtx;
std::ofstream Logger::file("app.log", std::ios::app);

void Logger::log(const std::string& msg) {
    std::lock_guard<std::mutex> lock(mtx);
    file << msg << std::endl;
}

void Logger::clear() {
    std::lock_guard<std::mutex> lock(mtx);

    // Close the current file stream
    file.close();

    // Reopen in truncate mode to clear contents
    file.open("app.log", std::ios::trunc);

    // Immediately switch back to append mode for normal logging
    file.close();
    file.open("app.log", std::ios::app);
}


