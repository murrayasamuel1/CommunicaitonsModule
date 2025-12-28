//
// Created by murra on 12/21/2025.
//

#ifndef V1_LOGGER_H
#define V1_LOGGER_H
// logger.h
#pragma once
#include <fstream>
#include <mutex>
#include <string>

class Logger {
public:
    static void log(const std::string& msg);
    static void clear();

private:
    static std::mutex mtx;
    static std::ofstream file;
};


#endif //V1_LOGGER_H

