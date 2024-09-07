
import cv2 as cv
import numpy as np
import pyautogui
import time
from threading import Thread
import os
from screeninfo import get_monitors


###nur hauptscreen verwenden und ggf anpassen 
def get_primary_monitor():
    for m in get_monitors():
        if m.is_primary:
            return m
    return None

scaling_factor = 1  # Manuell für Retina Displays

def move_cursor_within_primary(x, y):
    primary_monitor = get_primary_monitor()
    if primary_monitor:
        # Anpassen der Koordinaten basierend auf dem DPI-Skalierungsfaktor
        x *= scaling_factor
        y *= scaling_factor

        # Verschiebe innerhalb der Grenzen des primären Monitors
        adjusted_x = primary_monitor.x + max(0, min(x, primary_monitor.width))
        adjusted_y = primary_monitor.y + max(0, min(y, primary_monitor.height))
        pyautogui.moveTo(adjusted_x, adjusted_y)

class FishingAgent:
    def __init__(self, main_agent)-> None: 
        self.main_agent = main_agent 
        self.fishing_target = cv.imread("/Users/magnus/Documents/fishersfritz/fishing/assets/fishing_target.png")
        self.fishing_thread = None

    def cast_lure(self):
        print("Casting!...")
        # pyautogui.press('1')
        time.sleep(2)
        self.find_lure()

    def find_lure(self):
     if self.main_agent.cur_img is not None:
        cur_img = self.main_agent.cur_img
        lure_location = cv.matchTemplate(
            cur_img, 
            self.fishing_target,
            cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(lure_location)
        
        # Ergebnisbild für die Darstellung
        result_img = cur_img.copy()

        # Berechnung der Position des Rechtecks
        top_left = max_loc
        bottom_right = (top_left[0] + self.fishing_target.shape[1], top_left[1] + self.fishing_target.shape[0])

        # Zeichnen eines Rechtecks um den gefundenen Bereich
        cv.rectangle(result_img, top_left, bottom_right, (0, 255, 0), 2)

        # Markieren des Zentrums
        center = (top_left[0] + (bottom_right[0] - top_left[0]) // 2, top_left[1] + (bottom_right[1] - top_left[1]) // 2)
        cv.drawMarker(result_img, center, (0, 0, 255), cv.MARKER_CROSS, markerSize=20, thickness=2)

        # Anzeigen des Ergebnisses
        cv.imshow("Match Template", result_img)
        cv.waitKey(0)
        print("Max location:", max_loc)
        print("Center location:", center)
        self.move_to_lure(center)


        
        
    def move_to_lure(self, center_loc):
    # max_loc ist ein Tupel (x, y)
        move_cursor_within_primary(center_loc[0], center_loc[1])  # Tupel wird entpackt zu x und y


    def watch_lure(self):
        pass
    def pull_line(self):
        pass

    def run(self):
        while True:
            self.cast_lure()
            time.sleep(5)

