
import cv2 as cv
import numpy as np
import pyautogui
import time
from threading import Thread
from screeninfo import get_monitors
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
from scipy.signal import correlate
import logging
import faulthandler
faulthandler.enable()




screen_width, screen_height = pyautogui.size()
print("Reported screen size:", screen_width, "x", screen_height)

###nur hauptscreen verwenden und ggf anpassen 
def get_primary_monitor():
    for m in get_monitors():
        if m.is_primary:
            return m
    return None

scaling_factor = 1  # Manuell für Retina Displays




class FishingAgent:
    def __init__(self, main_agent)-> None: 
        self.main_agent = main_agent 
        self.fishing_target = cv.imread("/Users/magnus/Documents/fishersfritz/fishing/assets/fishing_target.png")
        self.fishing_thread = None
        self.bite_sound = AudioSegment.from_file("/Users/magnus/Documents/fishersfritz/bitesound.m4a")
        self.chunk = 2048
        self.sample_rate = 48000
        self.format = pyaudio.paInt16
        self.channels = 2
        self.p = pyaudio.PyAudio()
        self.device_index = 1  # BlackHole 2ch
    
    
    
    
    def cast_lure(self):
        time.sleep(2)
        pyautogui.press('1')
        print("Casting!...")
        time.sleep(2)
        center_loc = self.find_lure() #empty values == false like "" etc. 
        if center_loc:
            self.move_to_lure(center_loc)
            self.listen_for_bite()
        else:
            print("Lure nicht gefunden")
        
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
        
    def find_lure(self):
        if self.main_agent.cur_img is None or self.fishing_target is None:
            logging.error("Image or template is None.")
            return None

        cur_img = self.main_agent.cur_img
        template = self.fishing_target

        # Überprüfe und konvertiere Datentyp nur wenn nötig
        if cur_img.dtype != 'uint8':
            cur_img = np.uint8(cur_img * 255) if cur_img.max() <= 1.0 else np.uint8(cur_img)
        if template.dtype != 'uint8':
            template = np.uint8(template * 255) if template.max() <= 1.0 else np.uint8(template)

        try:
            lure_location = cv.matchTemplate(cur_img, template, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(lure_location)
            
            top_left = max_loc
            w, h = template.shape[1], template.shape[0]
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            center_loc = (center_x, center_y)

            logging.debug(f"Max location: {max_loc}")
            logging.debug(f"Center location: {center_loc}")
            return center_loc
        except Exception as e:
            logging.error(f"Error during matchTemplate: {e}")
            return None


    

    def move_to_lure(self, center_loc):
        duration = .1
        if center_loc:
            # Skalierungsverhältnis berechnen, basierend auf der Diskrepanz zwischen Screenshot- und Bildschirmauflösung
            scale_x = 1512 / 3024  # Bildschirmbreite / Screenshotbreite
            scale_y = 982 / 1964   # Bildschirmhöhe / Screenshothöhe

            # Koordinaten anpassen
            adjusted_x = int(center_loc[0] * scale_x)
            adjusted_y = int(center_loc[1] * scale_y)

            # Bewegen des Mauszeigers zu den angepassten Koordinaten
            pyautogui.moveTo(adjusted_x, adjusted_y,duration=duration, tween=pyautogui.easeOutQuad)
            time.sleep(.5)
            self.listen_for_bite()
            print(f"cursor moved to ({adjusted_x}, {adjusted_y})")
        else:
            print("no valid cords found")

    def listen_for_bite(self):
        bite_detected = False
        watch_time = time.time()

        # Open PyAudio stream
        stream = self.p.open(format=self.format,
                             channels=self.channels,
                             rate=self.sample_rate,
                             input=True,
                             input_device_index=self.device_index,
                             frames_per_buffer=self.chunk)

        print("Listening for bite...")

        while not bite_detected and time.time() - watch_time < 20:  # Timeout nach 20 Sekunden
            # Lese Audio-Daten
            data = stream.read(self.chunk)
            current_sound = np.frombuffer(data, dtype=np.int16)
            current_sound = AudioSegment(
                current_sound.tobytes(), 
                sample_width=2, 
                frame_rate=self.sample_rate, 
                channels=self.channels
            )

            # Vergleiche den aktuellen Sound mit dem Biss-Sound
            correlation = self.compare_sounds(self.bite_sound, current_sound)
            if correlation > 0.9:  # Schwellenwert für Korrelation
                print("Bite detected!")
                bite_detected = True
                self.pull_line()
                break

        # Stoppe und schließe den Stream
        stream.stop_stream()
        stream.close()
        self.p.terminate()

    def compare_sounds(self, sound1, sound2):
        # Konvertiere AudioSegment in numpy Array
        sound1_data = np.array(sound1.get_array_of_samples())
        sound2_data = np.array(sound2.get_array_of_samples())

        # Berechne Kreuzkorrelation
        correlation = np.max(correlate(sound1_data, sound2_data, mode='valid'))
        return correlation

                
    def pull_line(self):
        print("pulling lure")
        pyautogui.rightClick()  # Simuliert das Einholen der Leine durch einen Rechtsklick
        time.sleep(1)  # Pausiert für 1 Sekunde nach dem Einholen der Leine
        self.cast_lure()  # Startet den Wurfprozess erneut


    def run(self):
        while True:
            self.cast_lure()
            time.sleep(5)




