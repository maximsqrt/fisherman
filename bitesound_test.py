from pydub import AudioSegment
from pydub.playback import play
import numpy as np

# Lade den Sound, der abgespielt wird, wenn ein Fisch anbeißt
bite_sound = AudioSegment.from_file("/Users/magnus/Documents/fishersfritz/bitesound.m4a")


# Funktion, um den Sound zu analysieren
def is_bite_sound(sound):
    # Hier kannst du eine Methode implementieren, um den Sound zu analysieren
    # und zu erkennen, ob es sich um den spezifischen Sound handelt.
    # Dies ist ein einfaches Beispiel, das die Länge des Sounds überprüft.
    return len(sound) == len(bite_sound)

# Beispiel für die Verwendung der Funktion
current_sound = AudioSegment.from_file("/Users/magnus/Documents/fishersfritz/bitesound.m4a")
if is_bite_sound(current_sound):
    print("Ein Fisch hat angebissen!")
    # Hier kannst du die gewünschte Aktion ausführen

from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import time

def listen_test(bite_sound_path, game_sound_path):
    # Lade den Sound, der abgespielt wird, wenn ein Fisch anbeißt
    bite_sound = AudioSegment.from_file(bite_sound_path)

    # Funktion, um den Sound zu analysieren
    def is_bite_sound(sound):
        # Hier kannst du eine Methode implementieren, um den Sound zu analysieren
        # und zu erkennen, ob es sich um den spezifischen Sound handelt.
        # Dies ist ein einfaches Beispiel, das die Länge des Sounds überprüft.
        return len(sound) == len(bite_sound)

    # Starte die Überwachung des Spielsounds
    watch_time = time.time()
    bite_detected = False

    while True:
        # Lade den aktuellen Spielsound
        current_sound = AudioSegment.from_file(game_sound_path)

        if is_bite_sound(current_sound):
            print("bite detected")
            bite_detected = True
            break  # Schleife verlassen, nachdem Biss erkannt wurde

        if time.time() - watch_time > 20:  # Timeout-Prüfung -one Period 30sec
            print("fishing timeout")
            break  # Schleife verlassen, nachdem Timeout erreicht ist

    if bite_detected or (time.time() - watch_time > 10):  # Prüfung, ob Bedingungen zum Beenden erfüllt wurden
        pull_line()  # Linie ziehen, nur einmal nach der Schleife

def pull_line():
    print("Linie wird gezogen!")
    # Hier kannst du die gewünschte Aktion ausführen
