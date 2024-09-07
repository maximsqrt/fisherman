import cv2 as cv
import numpy as np
import pyautogui
import time
from threading import Thread
import os
from screeninfo import get_monitors

class MonitorManager:
    def __init__(self):
        self.primary_monitor = self.get_primary_monitor()
        if self.primary_monitor:
            self.center_x = self.primary_monitor.x + self.primary_monitor.width // 2
            self.center_y = self.primary_monitor.y + self.primary_monitor.height // 2

    def get_primary_monitor(self):
        for monitor in get_monitors():
            if monitor.is_primary:
                return monitor
        return None

    def print_monitor_info(self):
        if self.primary_monitor:
            print(f"Monitor {self.primary_monitor.name}: Width={self.primary_monitor.width}, "
                  f"Height={self.primary_monitor.height}, X={self.primary_monitor.x}, "
                  f"Y={self.primary_monitor.y}, Is_primary={self.primary_monitor.is_primary}")
            print(f"Center of primary monitor: ({self.center_x}, {self.center_y})")
        else:
            print("No primary monitor found.")

    def move_cursor_to_center(self):
        if self.primary_monitor:
            pyautogui.moveTo(self.center_x, self.center_y)
            print(f"Cursor moved to: ({self.center_x}, {self.center_y})")

def main():
    manager = MonitorManager()
    manager.print_monitor_info()
    manager.move_cursor_to_center()

if __name__ == "__main__":
    main()
