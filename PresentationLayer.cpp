#include "PresentationLayer.h"
#include "logger.h"
#include "GS.pb.h"


// ETL includes




PresentationLayer::PresentationLayer() {


}

void PresentationLayer::tx() {
    while (true) {
        if (presentation_channel.pop(message))
        {
            Logger::log("AL: Received: " +message);

            V1::PropulsionCommand Propel;
            Propel.set_burn_time(10);
            Propel.set_burn_vector_x(10);
            Propel.set_burn_vector_y(10);
            Propel.set_burn_vector_z(10);
            Propel.set_type(V1::CommandType::Propulsion);

            std::string buffer;
            Propel.SerializeToString(&buffer);
            Logger::log("AL: Encoded: " + buffer);


        }
    }
}
    void PresentationLayer::rx(){
        while (true) {
            if (presentation_channel.pop(message))
            {
                Logger::log("AL: Received: " +message);

                V1::PropulsionCommand Propel;
                Propel.set_burn_time(10);
                Propel.set_burn_vector_x(10);
                Propel.set_burn_vector_y(10);
                Propel.set_burn_vector_z(10);
                Propel.set_type(V1::CommandType::Propulsion);

                std::string buffer;
                Propel.SerializeToString(&buffer);
                Logger::log("AL: Encoded: " + buffer);


            }
        }

}
