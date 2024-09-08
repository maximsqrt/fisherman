
import cv2 as cv
import numpy as np
import pyautogui
import time
from threading import Thread
import os
from screeninfo import get_monitors

import pyautogui

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

    def cast_lure(self):
        time.sleep(2)
        pyautogui.press('1')
        print("Casting!...")
        time.sleep(2)
        center_loc = self.find_lure() #empty values == false like "" etc. 
        if center_loc:
            self.move_to_lure(center_loc)
            self.watch_lure(center_loc)
        else:
            print("Lure nicht gefunden")
        
    def find_lure(self):
     if self.main_agent.cur_img is not None:
        cur_img = self.main_agent.cur_img
        template = self.fishing_target
        
        if cur_img.dtype != 'uint8':
             cur_img = cur_img.astype('uint8')
        if template.dtype != 'uint8':
             template = template.astype('uint8')
        
        lure_location = cv.matchTemplate(
            cur_img, 
            self.fishing_target,
            cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(lure_location)

        # Berechne das Zentrum des gefundenen Bereichs
        top_left = max_loc
        w, h = self.fishing_target.shape[1], self.fishing_target.shape[0]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        center_loc = (center_x, center_y)

        # Ergebnisbild für die Darstellung
        #result_img = cur_img.copy()

        # # Zeichnen eines Rechtecks um den gefundenen Bereich
        # cv.rectangle(result_img, top_left, bottom_right, (0, 255, 0), 2)

        # # Markieren des Zentrums
        # cv.drawMarker(result_img, center_loc, (0, 0, 255), cv.MARKER_CROSS, markerSize=20, thickness=2)
        # print("Max location:", max_loc)
        # print("Center location:", center_loc)
        # # Anzeigen des Ergebnisses
        # cv.imshow("Match Template", result_img)
        # cv.waitKey(0)  # Warte auf eine Taste
        # cv.destroyAllWindows()  # Schließe das Fenster

        print("max location:", max_loc)
        print("center location:", center_loc)
        print("center_loc returned")
        return center_loc  # Gib die berechneten Koordinaten zurück
     else:
        print("no lure detected")
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
            self.watch_lure(center_loc)
            print(f"cursor moved to ({adjusted_x}, {adjusted_y})")
        else:
            print("no valid cords found")





    def watch_lure(self, center_loc):
        time.sleep(3)
        initial_image = self.main_agent.cur_imgHSV
        watch_time = time.time()
        bite_detected = False  # Zustandsvariable zur Überwachung der Biss-Erkennung

        while True:
            current_image = self.main_agent.cur_imgHSV
            pixel_change = cv.absdiff(initial_image[center_loc[1], center_loc[0]], current_image[center_loc[1], center_loc[0]])

            if np.sum(pixel_change) > 130:  # Schwelle für Biss-Erkennung
                print("bite detected")
                bite_detected = True
                break  # Schleife verlassen, nachdem Biss erkannt wurde
            
            if time.time() - watch_time > 20:  # Timeout-Prüfung -one Period 30sec
                print("fishing timeout")
                break  # Schleife verlassen, nachdem Timeout erreicht ist

        if bite_detected or (time.time() - watch_time > 10):  # Prüfung, ob Bedingungen zum Beenden erfüllt wurden
            self.pull_line()  # Linie ziehen, nur einmal nach der Schleife


                
    def pull_line(self):
        print("pulling line")
        pyautogui.rightClick()  # Simuliert das Einholen der Leine durch einen Rechtsklick
        time.sleep(1)  # Pausiert für 1 Sekunde nach dem Einholen der Leine
        self.cast_lure()  # Startet den Wurfprozess erneut


    def run(self):
        while True:
            self.cast_lure()
            time.sleep(5)

