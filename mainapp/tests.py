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

def listen():
    global devboard
    while True:
        if devboard:
            try:
                mes = devboard.readline().decode('utf-8', errors='ignore').strip()

                print(mes)
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

#threading.Thread(target=listen, daemon=True).start()
listen()