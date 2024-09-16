
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
import gc

def list_audio_devices(self):
    num_devices = self.p.get_device_count()
    for i in range(num_devices):
        dev_info = self.p.get_device_info_by_index(i)
        print(f"Device {i}: {dev_info.get('name')}")

# Right Device? 
logging.debug("Opening audio stream...")
# PyAudio operations
logging.debug("Audio stream opened successfully.")


screen_width, screen_height = pyautogui.size()
print("Reported screen size:", screen_width, "x", screen_height)

### Use only mainscreen 
def get_primary_monitor():
    for m in get_monitors():
        if m.is_primary:
            return m
    return None

scaling_factor = 1  # Manuell for Retina :( )



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
        center_loc = self.find_lure() #empty values == false like "" etc. 1
        print(center_loc)
        if center_loc:
            self.move_to_lure(center_loc)
            #no listen_for_bite in cast_lure
        else:
            print("Lure nicht gefunden")
        
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
        
    def find_lure(self):
        if self.main_agent.get_cur_img() is None or self.fishing_target is None:
            logging.error("Current image or fishing target template is not available.")
            return None

        cur_img = self.main_agent.get_cur_img()
        logging.debug(f"Original image dtype: {cur_img.dtype}, shape: {cur_img.shape}, max value: {cur_img.max()}")

        # Ensure both images are in the correct data type and scale
        if cur_img.dtype != 'uint8':
            cur_img = np.uint8(cur_img * 255) if cur_img.max() <= 1.0 else np.uint8(cur_img)
        if self.fishing_target.dtype != 'uint8':
            self.fishing_target = np.uint8(self.fishing_target * 255) if self.fishing_target.max() <= 1.0 else np.uint8(self.fishing_target)

        logging.debug(f"Converted image dtype: {cur_img.dtype}, shape: {cur_img.shape}")
        

        # Apply template matching to find the lure
           
        try:
            result = cv.matchTemplate(cur_img, self.fishing_target, cv.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv.minMaxLoc(result)
            logging.debug(f"MatchTemplate max_val: {max_val}, max_loc: {max_loc}")

            if max_val < 0.6:
                logging.debug("Lure not found, max correlation value below threshold.")
                return None

            top_left = max_loc
            w, h = self.fishing_target.shape[1], self.fishing_target.shape[0]
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            center_loc = (center_x, center_y)

            logging.debug(f"Lure found at position: {center_loc} with max correlation value: {max_val}")
            return center_loc
        except Exception as e:
            logging.error(f"Error during template matching: {e}")
            return None



    

    def move_to_lure(self, center_loc):
        duration = .1
        if center_loc:
            # Scaling Ratio based on the discrepancy between screenshot and screen resolution
            scale_x = 1512 / 3024  # W / H 
            scale_y = 982 / 1964   # W / H

            # Koordinaten anpassen
            adjusted_x = int(center_loc[0] * scale_x)
            adjusted_y = int(center_loc[1] * scale_y)

            # MOVE CURSOR slighty fast, check later.. 
            pyautogui.moveTo(adjusted_x, adjusted_y,duration=duration, tween=pyautogui.easeOutQuad)
            time.sleep(.5)
            self.listen_for_bite()
            print(f"cursor moved to ({adjusted_x}, {adjusted_y})")
        else:
            print("no valid cords found")

    #initialise pyaudio.PyAudio in listen_for_bite 
    def listen_for_bite(self):
        bite_detected = False
        watch_time = time.time()

        # Initialize variables
        p = None
        stream = None

        try:
            p = pyaudio.PyAudio()  # Create the PyAudio instance here
            stream = p.open(format=self.format,
                            channels=self.channels, 
                            rate=self.sample_rate,
                            input=True,
                            input_device_index=self.device_index,
                            frames_per_buffer=self.chunk)
            logging.debug("Audio stream opened successfully.")
            print("Listening for bite...")

            while not bite_detected and time.time() - watch_time < 20:  # Timeout after 20 seconds
                # Read audio data
                data = stream.read(self.chunk, exception_on_overflow=False)
                current_sound = np.frombuffer(data, dtype=np.int16)
                current_sound = AudioSegment(
                    current_sound.tobytes(), 
                    sample_width=2, 
                    frame_rate=self.sample_rate, 
                    channels=self.channels
                )

                # Initialize correlation to None
                correlation = None

                try:
                    # Compare current sound to bite sound
                    correlation = self.compare_sounds(self.bite_sound, current_sound)
                    logging.debug(f"Correlation value: {correlation}")
                    
                    # Protokolliere den Korrelationswert in eine Datei oder Konsole
                    with open("correlation_values.txt", "a") as f:
                        f.write(f"{time.time()},{correlation},{bite_detected}\n")

                except Exception as e:
                    logging.error(f"Error comparing sounds: {e}")
                    continue  # Skip to the next iteration

                if correlation is not None and correlation > 0.1:  # Temporär Schwellenwert auf 0 setzen, um alle Werte zu erfassen
                    print(f"Correlation value: {correlation}")
                    # Noch nicht auf Bite detected setzen

        except Exception as e:
            logging.error(f"Error during audio processing: {e}")

        finally:
            # Ensure the stream is closed properly
            if stream is not None:
                stream.stop_stream()
                stream.close()
            if p is not None:
                p.terminate()
                logging.debug("Audio stream closed.")

        # Entferne vorübergehend das automatische Ziehen der Angel, um Fehlalarme zu vermeiden
        # if bite_detected:
        #     self.pull_line()




    def compare_sounds(self, sound1, sound2):
        # Konvertiere Audio in Arrays
        sound1_data = np.array(sound1.get_array_of_samples()).astype(np.float32)
        sound2_data = np.array(sound2.get_array_of_samples()).astype(np.float32)

        # Sicherstellen, dass beide Arrays die gleiche Länge haben
        min_len = min(len(sound1_data), len(sound2_data))
        sound1_data = sound1_data[:min_len]
        sound2_data = sound2_data[:min_len]

        # Berechne die normierte Kreuzkorrelation
        numerator = np.correlate(sound1_data, sound2_data, mode='valid')[0]
        denominator = np.sqrt(np.correlate(sound1_data, sound1_data, mode='valid')[0] * np.correlate(sound2_data, sound2_data, mode='valid')[0])
        if denominator == 0:
            return 0
        correlation = numerator / denominator

        return correlation





    

                
    def pull_line(self):
        print("pulling lure")
        pyautogui.rightClick()  #Pull "fish"
        time.sleep(.2)  # short pause 
        self.cast_lure()  # cast lure again


    def run(self):
        while True:
            self.cast_lure()
            time.sleep(5)




