Home Automation System

A custom, end-to-end Smart Home ecosystem built from the ground up—spanning custom hardware electronics, core server architecture, low-latency wireless communication, and cross-platform user applications.

Project Overview

This project is an attempt to build a fully self-hosted, modular Smart Home ecosystem without relying on off-the-shelf proprietary solutions.

The system leverages a Raspberry Pi 5 as the central computing and orchestrating server. Communication with edge devices is handled via UART linked to a primary ESP transmitter,
which establishes a fast, lightweight ESP-NOW mesh network to communicate directly with distributed node modules throughout the home.

System Architecture

[ Web Web App / Desktop App ]                                  
             │                                                                        
             ▼                                                                  
      [ Raspberry Pi 5 ] (Central Server)                                                    
             │ (UART Serial)                                                                                            
             ▼                                                      
     [ ESP Transmitter ]                                                                                                    
             │ (ESP-NOW Protocol)                                                                                            
      ┌──────┼──────┐                                                  
                                            
   [Node]  [Node]  [Node] ... (Relays, Sensors, Controllers)                      


Central Server (Raspberry Pi 5): Handles core logic, data processing, user authentication, and interfaces with front-end clients.

Serial Bridge (UART): Bridges the central server to the wireless transmitter with minimal latency.

Wireless Network (ESP-NOW): A low-power, peer-to-peer protocol connecting all remote nodes (on/off switches, sensors, and controllers) into a flexible mesh-like network.

Client Applications: Web dashboard and desktop applications for remote monitoring and control.

Key Features

Full-Stack Custom Ecosystem: Built entirely from scratch—from microcontrollers to UI interfaces.

Ultra-Low Latency: ESP-NOW protocol ensures instant transmission between nodes and the primary hub.

Cross-Platform Access: Control and monitor device states via a web web interface or dedicated desktop application.

Modular Hardware Design: Easily expandable to support new ESP-based sensor or relay nodes.

Centralized Control: Raspberry Pi 5 orchestrates all automation routines and state persistence.

Tech Stack & Hardware

Hardware:

Raspberry Pi 5 (Central Server)

ESP32 Microcontrollers

Relays, Sensors & Custom Electronic Circuits

Protocols & Communication:

ESP-NOW (Node-to-Node / Node-to-Transmitter)

UART / Serial (Transmitter-to-Pi Server Interface)

Software & Applications:

Web Interface: Modern responsive frontend for web browser control

Desktop Application: Cross-platform app for quick access from desktop OS

