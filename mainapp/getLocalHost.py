from flask import Flask, request, render_template, jsonify
import threading
from mainapp import config
import time

server = None
runing_host = False

def run_host():
    app = Flask(__name__)

    @app.before_request
    def log_request():
        print(f"{request.remote_addr} - {request.method} {request.path}")

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/wlacz_lampa')
    def wlacz_lampa():
        print("Włączono urządzenie!")
        config.lampa_mode = True
        return "lampa włączone!"

    @app.route('/wylacz_lampa')
    def wylacz_lampa():
        print("Wyłączono urządzenie!")
        config.lampa_mode = False
        return "lampa wyłączone!"

    @app.route('/wlacz_led')
    def wlacz_led():
        config.ledy_mode = True
        return "ledy włączone"
    @app.route('/wylacz_led')
    def wylacz_led():
        config.ledy_mode = False
        return "ledy wyłączone"
    @app.route('/odsłoń')
    def odsłon():
        config.motor_up_state = True
        config.motor_down_state = False
        return "odsłaniam"
    @app.route('/stop')
    def stop():
        config.motor_up_state = False
        config.motor_down_state = False
        return "stop"
    @app.route('/zasłoń')
    def zasłoń():
        config.motor_up_state = False
        config.motor_down_state = True
        return "zasłaniam"


    @app.route("/state")
    def state_manager():
        config.website_is_connected = True
        config.last_connection_time = time.time()

        response = {
            "ledy": "włączone" if config.ledy_mode else "wyłączone",
            "lampa": "włączona" if config.lampa_mode else "wyłączona",
            "website": "połączony" if config.website_is_connected else "rozłączony"

        }
        #if response:
        #    config.website_is_connected = True
        #else:
         #   config.website_is_connected = False
        #config.website_is_connected = True
        return jsonify(response)
    #config.website_is_connected = False

    def monitor_connections(timeout=1):
        while True:
            if time.time() - config.last_connection_time > timeout:
                config.website_is_connected = False
            time.sleep(1)

    threading.Thread(target=monitor_connections, daemon=True).start()

    #---------------------------- klient - serwer intrafce -----------------------------
    #funckja odbierajaca
    @app.route("/get_states", methods=["GET"])
    def get_states():
        config.comp2_is_connected = True
        config.last_connection_for_comp2 = time.time()
        return jsonify({
            "ledy_mode": config.ledy_mode,
            "lampa_mode": config.lampa_mode,
            "motor_up_state": config.motor_up_state,
            "motor_down_state": config.motor_down_state,
            "gniazdo2_mode": config.gniazdo2_mode,
            # dopisz inne stany
        })
    def monitor_comp2(timeout=1):
        while True:
            if time.time() - config.last_connection_time > timeout:
                config.comp2_is_connected = False
            time.sleep(1)
    threading.Thread(target=monitor_comp2, daemon=True).start()
    #funkcja nadawcza
    @app.route("/set_states", methods=["POST"])
    def set_states():
        data = request.get_json(silent=True) or {}

        if "ledy_mode" in data:
            config.ledy_mode = bool(data["ledy_mode"])
        if "lampa_mode" in data:
            config.lampa_mode = bool(data["lampa_mode"])
        if "motor_up_state" in data:
            config.motor_up_state = bool(data["motor_up_state"])
        if "motor_dwon_sate" in data:
            config.motor_down_state = bool(data["motor_down_state"])
        if "gniazdo2_mode" in data:
            config.gniazdo2_mode = bool(data["gniazdo2_mode"])


        if "serial_is_connected" in data:
            config.serial_is_connected = bool(data["serial_is_connected"])
        if "comp1_is_connected" in data:
            config.comp1_is_connected = bool(data["comp1_is_connected"])
        if "website_is_connected" in data:
            config.website_is_connected = bool(data["website_is_connected"])
        if "mod1_is_connected" in data:
            config.mod1_is_connected = bool(data["mod1_is_connected"])
        if "mod2_is_connected" in data:
            config.mod2_is_connected = bool(data["mod2_is_connected"])

        # Zawsze zwracamy odpowiedź JSON
        return jsonify({
            "ledy_mode":                 config.ledy_mode,
            "lampa_mode":                config.lampa_mode,
            "motor_up_state":            config.motor_up_state,
            "motor_down_state":          config.motor_down_state,
            "gniazdo2_mode":                  config.gniazdo2_mode,

            "serial_is_connected":       config.serial_is_connected,
            "comp1_is_connected":        config.comp1_is_connected,
            "website_is_connected":      config.website_is_connected,
            "mod1_is_connected":         config.mod1_is_connected,
            "mod2_is_connected":         config.mod2_is_connected
        })

    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':

    threading.Thread(target=run_host, daemon=True).start()

    print("Serwer działa w tle. Otwórz http://localhost:5000")

    while True:
        time.sleep(1)