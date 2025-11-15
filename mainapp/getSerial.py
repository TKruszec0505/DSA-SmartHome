import serial
import serial.tools.list_ports
from mainapp import config
import time


def find_device():
    vid = 6790
    pid = 29987
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if p.vid == vid and p.pid == pid:
            return p.device
    return None

port = find_device()
#port = 'COM4'
baudrate = 9600


try:
    devboard = serial.Serial(port, baudrate, timeout=1)
    config.serial_is_connected = True
    print("polaczono")
except serial.SerialException as e:
    config.serial_is_connected = False
    devboard = None
    print(e)

def message(name):
    if devboard:
        devboard.write(f'{name}\n'.encode())
        print(name)
def check_states_start():
    if devboard:
        message('status?mod1')
        message('status?mod2')
def lamp_mode_sync_loop():
    last_state = config.lampa_mode
    while True:
        if config.lampa_mode != last_state:
            if config.lampa_mode:
                message('lampon')
            else:
                message('lampoff')
            last_state = config.lampa_mode
        time.sleep(0.2)
def led_mode_sync_loop():
    last_state = config.ledy_mode
    while True:
        if config.ledy_mode != last_state:
            if config.ledy_mode:
                message('ledon')
            else:
                message('ledoff')
            last_state = config.ledy_mode
        time.sleep(0.2)
def gniazdo2_mode_sync_loop():
    last_state = config.gniazdo2_mode
    while True:
        if config.gniazdo2_mode != last_state:
            if config.gniazdo2_mode:
                message('gniazdoon')
            else:
                message('gniazdooff')
            last_state = config.gniazdo2_mode
        time.sleep(0.2)


def motor_sync_loop():
    last_state_up = config.motor_up_state
    last_state_down = config.motor_down_state
    while True:
        if config.motor_up_state != last_state_up:
            if config.motor_up_state:

                message('motorup')
            else:
                message('motoroff')
            last_state_up = config.motor_up_state
        if config.motor_down_state != last_state_down:
            if config.motor_down_state:
                message('motordown')
            else:
                message('motoroff')
            last_state_down = config.motor_down_state
        time.sleep(0.2)


def listen_for_devboard():
    global devboard
    while True:
        if devboard:
            try:

                mes = devboard.readline().decode('utf-8', errors='ignore').strip()
                #print([hex(b) for b in msg])
                #print(mes)
                if "Awaria led" in mes:
                    print(mes)
                elif mes == "LAMP_ON":
                    print(mes + "s")
                    config.lampa_mode = True

                    config.mod1_is_connected = True
                elif mes == "LAMP_OFF":
                    print(mes +"S")
                    config.lampa_mode = False

                    config.mod1_is_connected = True
                elif mes == "LED_ON":
                    print(mes + "s")
                    config.ledy_mode = True

                    config.mod2_is_connected = True
                elif mes == "LED_OFF":
                    print(mes + "s")
                    config.ledy_mode = False
                    config.mod2_is_connected = True
                elif mes == "GNIAZDO2_ON":
                    config.gniazdo2_mode = True
                    config.mod2_is_connected = True
                elif mes == "GNIAZDO2_OFF":
                    config.gniazdo2_mode = False
                    config.mod2_is_connected = True
                elif mes =="motor_up":
                    print(mes + "s")
                    config.motor_up_state = True
                    config.motor_down_state = False
                elif mes =="motor_down":
                    print(mes + "s")
                    config.motor_down_state = True
                    config.motor_up_state = False
                elif mes == "motor_off":
                    print(mes + "s")
                    config.motor_down_state = False
                    config.motor_up_state = False
                elif "Temp:" in mes:
                    print(mes)
                elif mes=="pong2":
                    #print(mes + "s")
                    config.mod2_is_connected = True
                elif mes != "pong2":
                    config.mod2_is_connected = False
                elif mes == "pong1":
                    config.mod1_is_connected = True
                elif mes != "pong1":
                    config.mod1_is_connected = False



            except serial.SerialException as er:
                print(f"[DISCONNECTED] {er}")
                config.serial_is_connected = False
                try:
                    devboard.close()
                except Exception:
                    pass
                devboard = None

        else:
            config.serial_is_connected = False
            time.sleep(1)
            port = find_device()
            if port:
                try:
                    devboard = serial.Serial(port, baudrate, timeout=1)
                    config.serial_is_connected = True
                    print("[RECONNECTED] polaczono ponownie")
                except serial.SerialException as er:
                    print(f"nie udalo sie otworzyc: {er}")
                    devboard = None