#########
##   __  
## >(o )___ 
##  (   .  ) 
##~~~~~~~~~~~



import numpy as np
import cv2 as cv
import time
import mss
from threading import Thread, Lock
from fishing.fishing_agent import FishingAgent
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

def update_screen(agent):
    global shared_screenshot
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        t0 = time.time()
        fps_report_delay = 5
        fps_report_time = time.time()
        while True:
            with agent.lock:
                agent.cur_img = np.array(sct.grab(monitor))
                if agent.cur_img.size == 0:
                    print("Screenshot is invalid")
                    continue
            shared_screenshot = cv.cvtColor(agent.cur_img, cv.COLOR_BGRA2BGR)
            agent.cur_img = shared_screenshot
            agent.cur_imgHSV = cv.cvtColor(agent.cur_img, cv.COLOR_BGR2HSV)
            ex_time = time.time() - t0
            if time.time() - fps_report_time >= fps_report_delay:
                print("fps: " + str(1 / ex_time))
                fps_report_time = time.time()
            t0 = time.time()
            time.sleep(0.005)

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
    main_agent = MainAgent()
    update_screen_thread = Thread(target=update_screen, args=(main_agent,), daemon=True)
    update_screen_thread.start()
    user_input_thread = Thread(target=user_input_handler, args=(main_agent,), daemon=True)
    user_input_thread.start()

    display_screen()  # Run display_screen in the main thread

    update_screen_thread.join()
    user_input_thread.join()  # Wait for user input thread to finish if needed
    logging.info("Application shutdown.")
