#########
##   __  
## >(o )___ 
##  (   .  ) 
##~~~~~~~~~~~1
import logging
import os
print("Current working directory:", os.getcwd())



# Übernimm genau diese Konfiguration
log_filename = 'app.log'
log_path = os.path.join(os.getcwd(), log_filename)  # Überprüfe und stelle sicher, dass das Verzeichnis korrekt ist

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_path,
    filemode='w'
)

logging.debug("Logging im Hauptprojekt ist nun aktiv.")
print("Logging sollte jetzt aktiv sein. Überprüfe die Datei:", log_path)

import numpy as np
import cv2 as cv
import time
import mss
from threading import Thread, Lock
from fishing.fishing_agent import FishingAgent
import logging
from memory_profiler import memory_usage
# Configure logging





shared_screenshot = None

class MainAgent:
    def __init__(self) -> None:
        self.lock = Lock()
        self.agents = []
        self.fishing_thread = None
        self.cur_img = None  # BGR IMG
        self.cur_imgHSV = None  # HSV IMG
        self.zone = "Feralas"
        self.time = "night"
        print("MainAgent setup complete...")

    def get_cur_img(self):
        with self.lock:
            return self._cur_img if self._cur_img is not None else None

    def get_cur_imgHSV(self):
        with self.lock:
            return self._cur_imgHSV if self._cur_imgHSV is not None else None

    def set_cur_img(self, img):
        with self.lock:
            self._cur_img = img

    def set_cur_imgHSV(self, img):
        with self.lock:
            self._cur_imgHSV = img

def update_screen(agent):
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Monitor index might need to be adjusted based on your setup
        t0 = time.time()
        initial_memory = memory_usage()  # Measure initial memory usage
        fps_report_time = time.time()
        fps_report_delay = 5  # Interval in seconds to report FPS

        while True:
            screenshot = np.array(sct.grab(monitor))
            if screenshot.size == 0:
                print("Screenshot is invalid")
                continue
            
            # Convert the screenshot to BGR format
            shared_screenshot = cv.cvtColor(screenshot, cv.COLOR_BGRA2BGR)
            # Convert the BGR image to HSV format
            screenshot_hsv = cv.cvtColor(shared_screenshot, cv.COLOR_BGR2HSV)

            # Use setter methods to update the images in the main agent
            agent.set_cur_img(shared_screenshot)
            agent.set_cur_imgHSV(screenshot_hsv)

            # Calculate the execution time for performance monitoring
            ex_time = time.time() - t0  # Time since last frame
            current_memory = memory_usage()[0] - initial_memory[0]  # Memory used since start

            # Report FPS every 5 seconds
            if time.time() - fps_report_time >= fps_report_delay:
                if ex_time > 0:
                    print(f"FPS: {1 / ex_time:.2f}")
                fps_report_time = time.time()
            # print(f"Execution time: {ex_time:.2f} seconds")
            # print(f"Memory used: {current_memory:.2f} MiB")
            # Reset the timer for the next frame
            t0 = time.time()
            time.sleep(0.005)  # Small sleep to prevent excessive CPU usage


def display_screen():
    global shared_screenshot, main_agent
    last_display_state = None  # Track the last display state
    
    logging.debug("Starting display_screen loop.")
    while True:
        main_agent.lock.acquire()
        try:
            if shared_screenshot is not None:
                if last_display_state != "displaying":
                    logging.debug("Displaying image.")
                    last_display_state = "displaying"
                # Displayshow 
                # cv.imshow("Computer Vision", shared_screenshot)
            else:
                if last_display_state != "no_display":
                    logging.debug("No screenshot available to display.")
                    last_display_state = "no_display"
        finally:
            main_agent.lock.release()

        if cv.waitKey(1) == ord('q'):
            logging.info("Quit key pressed.")
            break

        time.sleep(0.005)


def print_menu():
    print("Enter a command:")
    print("\tS\tStart the main agent.")
    print("\tZ\tSet Zone")
    print("\tF\tStart Fishing Agent")
    print("\tQ\tQuit ???")

def user_input_handler(main_agent):
    while True:
        print_menu()
        user_input = input("Please enter a command: ").lower().strip()

        if user_input == "s":
            if main_agent.update_screen_thread is None or not main_agent.update_screen_thread.is_alive():
                print("Starting main agent screen update thread...")
                main_agent.update_screen_thread = Thread(target=update_screen, args=(main_agent,), daemon=True)
                main_agent.update_screen_thread.start()
            else:
                print("Main agent screen update thread is already running.")

        elif user_input == "f":
            if main_agent.fishing_thread is None or not main_agent.fishing_thread.is_alive():
                print("Starting Fishing Agent...")
                fishing_agent = FishingAgent(main_agent)
                main_agent.fishing_thread = Thread(target=fishing_agent.run, daemon=True)
                main_agent.fishing_thread.start()
            else:
                print("Fishing Agent is already running.")

        elif user_input == "z":
            print("Zone setting feature not implemented yet.")
        
        elif user_input == "q":
            cv.destroyAllWindows()
            break

        else:
            print("Input error. Please try again.")




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    main_agent = MainAgent()
    update_screen_thread = Thread(target=update_screen, args=(main_agent,), daemon=True)
    update_screen_thread.start()
    user_input_thread = Thread(target=user_input_handler, args=(main_agent,), daemon=True)
    user_input_thread.start()

    display_screen()  # Run display_screen in the main thread

    update_screen_thread.join()
    user_input_thread.join()  # Wait for user input thread to finish if needed
    logging.info("Application shutdown.")
