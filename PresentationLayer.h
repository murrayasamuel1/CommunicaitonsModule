#pragma once
#include "etl/queue_mpmc_mutex.h"
#include "etl/string.h"

class PresentationLayer {
    //constructor
public:
    PresentationLayer();
    void tx();
    void rx();
    inline static etl::queue_mpmc_mutex<std::string, 10> presentation_channel{};

private:
    inline static std::string message{};

};
