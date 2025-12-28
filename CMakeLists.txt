cmake_minimum_required(VERSION 3.21)
project(V1)

set(CMAKE_CXX_STANDARD 20)

find_package(Protobuf CONFIG REQUIRED)

# Generate protobuf sources
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS
        ${CMAKE_SOURCE_DIR}/GS.proto
)

# Make generated headers visible
include_directories(${CMAKE_CURRENT_BINARY_DIR})

# -------------------------
# V1 Executable
# -------------------------
add_executable(V1
        logger.cpp
        main.cpp
        PresentationLayer.cpp
        AppConnection.cpp
        ${PROTO_SRCS}
        ${PROTO_HDRS}
)

target_link_libraries(V1 PRIVATE protobuf::libprotobuf ws2_32)

# -------------------------
# GroundStationApplication
# -------------------------
add_executable(GroundStationApplication
        GroundStationApplication.cpp
        logger.cpp
        AppConnection.cpp
        Channel.h
        ${PROTO_SRCS}
        ${PROTO_HDRS}
)

target_link_libraries(GroundStationApplication PRIVATE protobuf::libprotobuf ws2_32)
