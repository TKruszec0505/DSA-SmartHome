cmake_minimum_required(VERSION 3.31)
project(DSA_SmartHome)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)
include_directories(clientapp)
include_directories(mainapp)

add_executable(DSA_SmartHome
        mainapp/testsC.cpp
        mainapp/main.cpp
)

# Jeśli używasz WiringPi na Pi
target_link_libraries(DSA_SmartHome wiringPi)

# Kopiowanie zasobów Python/WAV/PNG do katalogu build
file(COPY clientapp DESTINATION ${CMAKE_BINARY_DIR}/resources)

