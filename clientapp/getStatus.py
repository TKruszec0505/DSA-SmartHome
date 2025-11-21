import os
import time
import config

def network_checker():
    """
    Wątek sprawdzający dostępność urządzeń w sieci i aktualizujący config.
    """
    while True:
        # Ping comp1
        response = os.system("ping -n 1 192.168.100.10 >nul")  # podaj prawdziwe IP comp1
        config.comp1_is_connected = (response == 0)

        # comp2 - Twój komputer zawsze online
        config.comp2_is_connected = True

        # Ping website (przykład Google)
        response = os.system("ping -n 1 google.com >nul")
        config.website_is_connected = (response == 0)

        # Ping server
        response = os.system("ping -n 1 192.168.100.7 >nul")  # podaj prawdziwe IP serwera
        config.server_is_connected = (response == 0)

        # Ping mod1 i mod2 - tu możesz użyć prawdziwych adresów
        # response = os.system("ping -n 1 IP_mod1 >nul")
        # config.mod1_is_connected = (response == 0)
        # response = os.system("ping -n 1 IP_mod2 >nul")
        # config.mod2_is_connected = (response == 0)

        # Załóżmy motherboard online jeśli mod1 lub mod2 online
        config.motherboard_is_connected = config.mod1_is_connected or config.mod2_is_connected

        time.sleep(2)  # sprawdzanie co 2 sekundy