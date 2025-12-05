import threading
import time
import requests
import config

SERVER_URL = "http://192.168.100.15:5000"

lock = threading.Lock()
last_states_list = [config.ledy_mode,
                    config.lampa_mode,
                    config.gniazdo2_mode,
                    config.motor_up_state,
                    config.motor_down_state,

                    # aktualizacja stanu sieci
                    config.comp1_is_connected,
                    config.mod1_is_connected,
                    config.mod2_is_connected,
                    config.motherboard_is_connected,
                    config.server_is_connected,
                    config.website_is_connected]

def send_loop():
    global last_states_list
    while True:
        with lock:
            states_list = [config.ledy_mode,
                           config.lampa_mode,
                           config.gniazdo2_mode,
                           config.motor_up_state,
                           config.motor_down_state,

                           config.comp1_is_connected,
                           config.mod1_is_connected,
                           config.mod2_is_connected,
                           config.motherboard_is_connected,
                           config.server_is_connected,
                           config.website_is_connected]

            if states_list != last_states_list:
                last_states_list = states_list.copy()

                try:
                    requests.post(f"{SERVER_URL}/set_states", json={
                        "ledy_mode": config.ledy_mode,
                        "lampa_mode": config.lampa_mode,
                        "gniazdo2_mode": config.gniazdo2_mode,
                        "motor_up_state": config.motor_up_state,
                        "motor_down_state": config.motor_down_state,

                        #  "comp1_is_connected":           config.comp1_is_connected,
                        # "mod1_is_connected":            config.mod1_is_connected,
                        # "mod2_is_connected":            config.mod2_is_connected,
                        # "motherboard_is_connected":     config.motherboard_is_connected,
                        # "server_is_connected":          config.server_is_connected,
                        # "website_is_connected":         config.website_is_connected
                    }, timeout=3)

                    print("Wysłano stan do serwera:", config.ledy_mode, config.lampa_mode)

                except Exception as e:
                    print("Błąd wysyłania:", e)

        time.sleep(0.2)


def receive_loop():
    global last_states_list

    while True:
        try:
            response = requests.get(f"{SERVER_URL}/get_states", timeout=3).json()

            server_states_list = [
                response["ledy_mode"],
                response["lampa_mode"],
                response["gniazdo2_mode"],
                response["motor_up_state"],
                response["motor_down_state"],

                # sprawdz po przyjezdzie zgodnosc nazw(13.09)
                response["motherboard_is_connected"],
                response["comp1_is_connected"],
                response["website_is_connected"],
                response["mod1_is_connected"],
                response["mod2_is_connected"],
            ]

            with lock:
                if server_states_list != last_states_list:
                    (config.ledy_mode,
                     config.lampa_mode,
                     config.gniazdo2_mode,
                     config.motor_up_state,
                     config.motor_down_state,

                     config.comp1_is_connected,
                     config.mod1_is_connected,
                     config.mod2_is_connected,
                     config.motherboard_is_connected,
                     config.server_is_connected,
                     config.website_is_connected) = server_states_list

                    last_states_list = server_states_list.copy()

                    print("Zaktualizowano stan z serwera:", *server_states_list)

        except Exception as e:
            # print("(receive_loop) Błąd pobierania:", e)
            time.sleep(0)

        time.sleep(0.3)