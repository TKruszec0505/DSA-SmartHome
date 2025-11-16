import speech_recognition as sr
import pyautogui
import pyperclip
import time
import inflect
import threading
import wave
import pyaudio
import pyttsx3
import numpy as np
from mainapp import config, indexscript as ins

recognizer = sr.Recognizer()

audio_lock = threading.Event()

asisten_key = False
asisten_key_wrtie = False
asisten_key_open = False
neural_key = False

#---------------------------odgywanie dzwięków bez konfliktów niskopoziomowych(sterowniki karty dziwekowej)-------------
def play_sound(filename):
    audio_lock.set()
    try:
        wf = wave.open(filename, 'rb')
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                         channels=wf.getnchannels(),
                         rate=wf.getframerate(),
                         output=True)
        data = wf.readframes(1024)
        sampwidth = wf.getsampwidth()
        while data:
            if sampwidth == 2:
                samples = np.frombuffer(data, dtype=np.int16)
                samples = (samples * config.volume_val).astype(np.int16)
                data = samples.tobytes()
            stream.write(data)
            data = wf.readframes(1024)
        stream.stop_stream()
        stream.close()
        pa.terminate()
    finally:
        audio_lock.clear()
#-------------------------- funkcje upraszczajace ----------------------------------------------------------------------
def enginesay(say):
    engine = pyttsx3.init()
    engine.say(say)
    engine.runAndWait()
def lambda_for_commands(flag_name: str,state: bool, tekst_on: str, tekst_already_on: str) -> None:
    try:
        flag_value = getattr(config, flag_name)
        if not config.return_command_mode:
            setattr(config, flag_name, state)
        else:
            if not flag_value:
                setattr(config, flag_name, state)
                enginesay(tekst_on)
            else:
                enginesay(tekst_already_on)
    except AttributeError:
        print(f"Nie znaleziono flagi '{flag_name}' w config")
    except sr.UnknownValueError:
        print("nie rozumiem")

#--------------------------nasłuchiwanie i reagowanie na komendy-------------------------------------------------------
command_list = {
    "lampa_on":{
        "command": ["oświeć lampę","zaświeć lampę","włącz lampę"],
        "func": lambda: lambda_for_commands("lampa_mode",True,"oświetlam lampę","lampa już jest oświetlona"),
    },
    "lampa_off":{
        "command": ["zgaś lampę", "wyłącz lampę", "gaś lampę"],
        "func": lambda: lambda_for_commands("lampa_mode",False,"gaszę lampę","lampa jest już zgaszona")
    },
    "gniazdo_on":{
        "command": ["włącz gniazdo 1","włącz gniazdko 1 ","włącz gniazdo pierwsze","włącz gniazdko pierwsze","włącz gniazdko numer jeden"],
        "func": lambda: lambda_for_commands("ledy_mode",True,"włączam gniazdko numer jeden",
                                            "gniazdko numer jeden jest juz włączone")
    },
    "gniazdo_off":{
        "command": ["wyłącz gniazdo 1", "wyłącz gniazdko 1", "wyłącz gniazdo pierwsze", "wyłącz gniazdko pierwsze",
                    "wyłącz gniazdko numer jeden"],
        "func": lambda: lambda_for_commands("ledy_mode", False, "wyłączam gniazdko numer jeden",
                                            "gniazdko numer jeden jest juz wyłączone")
    },
    "gniazdo2_on":{
        "command": ["włącz gniazdo dwa","włącz gniazdko dwa","włącz gniazdo drugie","włącz gniazdko drugie","włącz gniazdko numer dwa","włącz gniazdko 2"],
        "func": lambda: lambda_for_commands("gniazdo2_mode", True, "włączam gniazdko numer dwa",
                                            "gniazdko numer dwa jest juz włączone")

    },
    "gniazdo2_off":{
        "command": ["wyłącz gniazdo dwa", "wyłącz gniazdko dwa", "wyłącz gniazdo drugie", "wyłącz gniazdko drugie",
                    "wyłącz gniazdko numer dwa"],
        "func": lambda: lambda_for_commands("gniazdo2_mode", False, "wyłączam gniazdko numer dwa",
                                            "gniazdko numer dwa jest juz wyłączone")
    },
    "odsłoń":{
        "command": ["odsłoń"," odsłoń rolete"," odsłoń okno"],
        "func": lambda: lambda_for_commands("motor_up_state", True, "odsłaniam",
                                            "okno już jest odsłaniane"),
        "func2": lambda: lambda_for_commands("motor_down_state", False, None,
                                            None)
    },
    "stop":{
        "command": ["stop"],
        "func": lambda: lambda_for_commands("motor_up_state", False, "wyłączam silnik",
                                            "silnik jest już wyłączony"),
        "func2": lambda: lambda_for_commands("motor_down_state", False, None,
                                            None)
    },
    "zasłoń":{
        "command": ["zasłoń","zasłoń rolete", "zasłoń okno"],
        "func": lambda: lambda_for_commands("motor_up_state", False, "zasłaniam",
                                            "okno już jest zasłaniane"),
        "func2": lambda: lambda_for_commands("motor_down_state", True, None,
                                             None)
    }
}
def listen_for_command():
    global asisten_key
    global asisten_key_wrtie
    global asisten_key_open
    global neural_key
    while audio_lock.is_set():
        time.sleep(1)
    with sr.Microphone() as source:
        print("Nasłuchiwanie hasła wybudzającego...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="pl-PL")
            print("Rozpoznano:", text)
            for item in command_list.values():
                if any(cmd in text.lower() for cmd in item["command"]):
                    item["func"]()
                    break

            if text.lower() == "dziękuję" or text.lower() == "dzięki":
                try:
                    if config.return_command_mode:
                        enginesay("nie ma za co")
                except sr.UnknownValueError:
                    print("nie rozumiem")
            if text.lower() == "szukaj":
                print("Wyszukiwanie aktywowane!")
                try:
                    # odtwarzanie dzwieku
                    threading.Thread(target=play_sound, args=("asystentscore.wav",)).start()
                    asisten_key = True
                except sr.UnknownValueError:
                    print("nie rozumiem")
            if text.lower() == "dyktuję":
                print("dyktowanie głosowe aktywowane!")
                try:
                    threading.Thread(target=play_sound, args=("asystentscore.wav",)).start()
                    asisten_key_wrtie = True
                except sr.UnknownValueError:
                    print("nie rozumiem")
            if text.lower() == "otwórz":
                print("Otwieranie aktywowane!")
                try:
                    threading.Thread(target=play_sound, args=("asystentscore.wav",)).start()
                    asisten_key_open = True
                except sr.UnknownValueError:
                    print("nie rozumiem")
#------------------------funkcje klawiszowe-----------------------------------------------------------------------------
            if text.lower() == "enter":
                print("enter")
                try:
                    threading.Thread(target=play_sound, args=("asystentscore2.wav",)).start()
                    pyautogui.press('enter')
                except sr.UnknownValueError:
                    print("nie rozumiem")
            if text.lower() == "skasuj":
                print("kasuje")
                try:
                    threading.Thread(target=play_sound, args=("asystentscore2.wav",)).start()
                    pyautogui.hotkey('ctrl', 'backspace')
                except sr.UnknownValueError:
                    print("nie rozumiem")
            if text.lower() == "screen":
                print("screenuje")
                try:
                    pyautogui.hotkey('windows', 'shift', 's')

                except sr.UnknownValueError:
                    print("nie rozumiem")
            if text.lower() == "klik":
                print("klik")
                try:
                    pyautogui.click(clicks=2)
                except sr.UnknownValueError:
                    print("nie rozumiem")
            if text.lower() == "weź":
                pyautogui.mouseDown()
            if text.lower() == "rzuć":
                pyautogui.mouseUp()
        except sr.UnknownValueError:
            print("Nie rozumiem.")
        except sr.RequestError as e:
            print("Błąd usługi rozpoznawania mowy:", e)
#-----------------------------------------wyłapywanie instrukcji po rozpoznaniu komendy---------------------------------
def listen_and_search():
    global asisten_key
    while audio_lock.is_set():
        time.sleep(1)
    with sr.Microphone() as source:
        print("Powiedz co chcesz wyszukać...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="pl-PL")
            print("Szukam:", text)
            pyperclip.copy(text)
            time.sleep(0.5)

            pyautogui.hotkey('ctrl', 'l')
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')

            if config.return_command_mode:
                engine = pyttsx3.init()
                engine.say(f"szukam  {text}")
                engine.runAndWait()
            else:
                pass

            asisten_key = False  # po wyszukaniu wraca

        except sr.UnknownValueError:
            print("Nie rozumiem co powiedziałeś")
        except sr.RequestError as e:
            print("Błąd usługi rozpoznawania mowy:", e)
def listen_and_write():
    global asisten_key_wrtie
    while audio_lock.is_set():
        time.sleep(1)
    with sr.Microphone() as source:
        print("Powiedz co chcesz napisać...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="pl-PL")
            print("Pisze:", text)
            pyperclip.copy(text)
            time.sleep(0.5)
            pyautogui.typewrite(text)
            asisten_key_wrtie = False
        except sr.UnknownValueError:
            print("Nie rozumiem co powiedziałeś")
        except sr.RequestError as e:
            print("Błąd usługi rozpoznawania mowy:", e)
def listen_and_open():
    global asisten_key_open
    while audio_lock.is_set():
        time.sleep(1)
    with sr.Microphone() as source:
        print("Powiedz co chcesz otworzyć...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="pl-PL")
            print("Otwieram:", text)
            ins.search_and_launch()
            threading.Thread(target=play_sound, args=("asystentscore.wav",)).start()
            asisten_key_open = False
        except sr.UnknownValueError:
            print("Nie rozumiem co powiedziales")
        except sr.RequestError as e:
            print("Błąd uslugi rozpoznawania mowy:", e)
#-----------------------------------numer do wyboru programu(tymczasowo tutaj)------------------------------------------
q = inflect.engine()
def listen_for_number():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="en-US")
            number = q.number_to_words(text)
            pyautogui.typewrite(number)
            print(number)
        except sr.RequestError as e:
            print("Błąd usługi rozpoznawania mowy:", e)
        except sr.UnknownValueError:
            print("nie rozumiem co powiedziałeś")
#-----------------------------------------petla wyzwalająca-------------------------------------------------------------
runing = False
def run_prog():
    global runing
    runing = True
    while runing:
        try:
            if not asisten_key and not asisten_key_wrtie and not asisten_key_open:
                print("Asystent głosowy uruchomiony!")
                print("Powiedz co mam zrobić: Wyszukać coć w operze - szukaj, napisać to co mowisz - dyktuje, otworzyc plik lub program - otwórz")
                listen_for_command()
                if asisten_key:
                    listen_and_search()
                    if not asisten_key:
                        continue
                if asisten_key_open:
                    listen_and_open()
                    if not asisten_key_open:
                        continue
                if asisten_key_wrtie:
                    listen_and_write()
                    if not asisten_key_wrtie:
                        continue
        except KeyboardInterrupt:
            break
