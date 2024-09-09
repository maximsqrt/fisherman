
############### falls audio nicht klappt ... 
# def pull_line():
    #     print("Linie wird gezogen!")
        # Hier kannst du die gewünschte Aktion ausführen

        # def watch_lure(self, center_loc):
        #     time.sleep(3)
        #     initial_image = self.main_agent.cur_imgHSV
        #     watch_time = time.time()
        #     bite_detected = False  # Zustandsvariable zur Überwachung der Biss-Erkennung

        #     while True:
        #         current_image = self.main_agent.cur_imgHSV
        #         pixel_change = cv.absdiff(initial_image[center_loc[1], center_loc[0]], current_image[center_loc[1], center_loc[0]])

        #         if np.sum(pixel_change) > 130:  # Schwelle für Biss-Erkennung
        #             print("bite detected")
        #             bite_detected = True
        #             break  # Schleife verlassen, nachdem Biss erkannt wurde
                
        #         if time.time() - watch_time > 20:  # Timeout-Prüfung -one Period 30sec
        #             print("fishing timeout")
        #             break  # Schleife verlassen, nachdem Timeout erreicht ist

        #     if bite_detected or (time.time() - watch_time > 10):  # Prüfung, ob Bedingungen zum Beenden erfüllt wurden
        #         self.pull_line()  # Linie ziehen, nur einmal nach der Schleife