import json
import shutil
import os
import subprocess as sp
import speech_recognition as sr
import inflect

recognizer = sr.Recognizer()

INDEX_FILE = "program_index.json"

q = inflect.engine()

SEARCH_DIRS = [
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
    r"C:\Windows\System32"
]

def build_index():
    index = []
    for folder in SEARCH_DIRS:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(".exe"):
                    index.append(os.path.join(root, file))
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    print(f"Zindeksowano {len(index)} plików EXE.")

def load_index():
    if not os.path.exists(INDEX_FILE):
        print("Brak indeksu — buduję...")
        build_index()
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def delete_and_update_index():

    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
        print("usuwam index")
    elif not os.path.exists(INDEX_FILE):
        load_index()



def search_and_launch(program_name):
    path = shutil.which(program_name)
    if path:
        print(f"Znaleziono w PATH: {path}")
        sp.Popen([path])
        return
    index = load_index()
    matches = []
    for p in index:
        filename = os.path.basename(p).lower()
        if program_name.lower() in filename:
            matches.append(p)
    if matches:
        if len(matches) == 1:
            sp.Popen([matches[0]])
            return
        print("Znaleziono kilka pasujących programów:")
        for i, match in enumerate(matches):
            print(f"{i + 1}. {match}")
        try:

            choice = int(input("Wybierz numer programu do uruchomienia: ", ))

            if 1 <= choice <= len(matches):
                sp.Popen([matches[choice - 1]])
            else:
                print("Nieprawidłowy wybór.")
        except:
            print("Nieprawidłowe dane.")
    else:
        print("Nie znaleziono programu w indeksie.")