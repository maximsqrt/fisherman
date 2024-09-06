import numpy as np      
import cv2 as cv
import time
import mss
from threading import Thread

shared_screenshot = None

class MainAgent: 
    def __init__(self) -> None:
        self.agents = []
        self.fishing_thread = None
        
        self.cur_img = None #BGR IMG
        self.cur_imgHSV = None #HSV IMG
        
        self.zone = "Feralas"
        self.time = "night"
        
        print("MainAgent setup complete...")

# Bildschirmaufnahme im separaten Thread
def update_screen(agent):
    global shared_screenshot
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        t0 = time.time()
        while True:
            # Bildschirm aufnehmen
            agent.cur_img = np.array(sct.grab(monitor))
            if agent.cur_img.size == 0:
                print("Screenshot is invalid")
                continue  
            shared_screenshot = cv.cvtColor(agent.cur_img, cv.COLOR_BGRA2BGR)
            agent.cur_img = cv.cvtColor(agent.cur_img, cv.COLOR_BGRA2BGR)
            agent.cur_imgHSV = cv.cvtColor(agent.cur_img, cv.COLOR_BGR2HSV)
            # FPS-Berechnung
            ex_time = time.time() - t0
            print("fps: " + str(1 / ex_time))
            t0 = time.time()

# Bildanzeige im Hauptthread
def display_screen():
    global shared_screenshot
    while True:
        if shared_screenshot is not None:
            cv.imshow("Computer Vision", shared_screenshot)

        # Beenden, wenn 'q' gedrückt wird
        key = cv.waitKey(1)
        if key == ord('q'):
            break

def print_menu():
    print("Enter a command:")
    print("\tS\tStart the main agent.")
    print("\tZ\tSet Zone")
    print("\tF\tStart Fishing Agent")
    print("\tQ\tQuit WOWZER")
    


if __name__ == "__main__":
    main_agent = MainAgent()
    print_menu()
    while True:
        user_input = input()
        user_input = str.lower(user_input).strip()
            
        if user_input == "s":
            pass
        if user_input == "z":
            pass
        if user_input == "f":
            pass
        if user_input == "q":
            break
        else: 
            print("input error")
            print_menu()
    print("exiting app")
    # Thread für die update_screen-Funktion erstellen
    update_screen_thread = Thread(
        target=update_screen, 
        args=(main_agent,),
        name="update_screen_thread",
        daemon=False  
    )

    # Starten des Bildschirmaufnahme-Threads
    update_screen_thread.start()
    print("Thread started")

    # Bildanzeige im Hauptthread
    display_screen()

    # Sicherstellen, dass der Thread beendet wird
    update_screen_thread.join()
    cv.destroyAllWindows()
