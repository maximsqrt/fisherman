import numpy as np
import cv2 as cv
import time
import mss

class MainAgent: 
    def __init__(self) -> None:
        self.screenshot = None

def update_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Verwende den Hauptmonitor
        
        while True: 
            # Startzeit für die gesamte Schleife
            t0 = time.time()

            # Zeitmessung für die Bildschirmaufnahme mit mss
            grab_start = time.time()
            screenshot = np.array(sct.grab(monitor))
            grab_time = time.time() - grab_start
            print(f"Zeit für Bildschirmaufnahme (mss): {grab_time:.6f} Sekunden")

            # Zeitmessung für die Farbkonvertierung
            color_start = time.time()
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGRA2BGR)  # mss gibt ein Bild mit einem Alpha-Kanal zurück
            color_time = time.time() - color_start
            print(f"Zeit für Farbkonvertierung: {color_time:.6f} Sekunden")

            # Zeitmessung für die Bildanzeige
            display_start = time.time()
            cv.imshow("Computer Vision", screenshot)
            display_time = time.time() - display_start
            print(f"Zeit für Bildanzeige: {display_time:.6f} Sekunden")

            # Taste abfragen
            key = cv.waitKey(1)
            if key == ord('q'):
                break

            # Gesamtzeit für einen Frame
            ex_time = time.time() - t0
            print(f"Gesamtzeit für einen Frame: {ex_time:.6f} Sekunden")
            print(f"FPS: {1 / ex_time:.2f}\n")

if __name__ == "__main__":
    update_screen()
