cmake_minimum_required(VERSION 3.31)
project(DSA_SmartHome)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)
include_directories(clientapp)
include_directories(firmware)
include_directories(mainapp)

add_executable(DSA_SmartHome
        clientapp/__init__.py
        clientapp/asystentscore.wav
        clientapp/asystentscore2.wav
        clientapp/config.py
        clientapp/getGraphs.py
        clientapp/getLocalHost.py
        clientapp/getPosision.py
        clientapp/indexscript.py
        clientapp/interface.py
        clientapp/qrcode1.png
        clientapp/script.py
        clientapp/ssRecognisionNN.py
        "firmware/module0 transmiter.cpp"
        firmware/Module1.cpp
        firmware/module2.cpp
        mainapp/testsC.cpp)
