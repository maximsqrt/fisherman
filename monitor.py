# from screeninfo import get_monitors

# def get_primary_monitor():
#     for m in get_monitors():
#         if m.is_primary:
#             return m
#     return None

# primary_monitor = get_primary_monitor()
# if primary_monitor:
#     print(f"Primary monitor: {primary_monitor.width}x{primary_monitor.height} at position ({primary_monitor.x}, {primary_monitor.y})")
# else:
#     print("No primary monitor detected.")



# def move_cursor_within_primary(x, y):
#     primary_monitor = get_primary_monitor()
#     if primary_monitor:
#         # Anpassen der Koordinaten auf Basis der Position des Hauptbildschirms
#         adjusted_x = primary_monitor.x + x
#         adjusted_y = primary_monitor.y + y
#         # Sicherstellen, dass die Koordinaten innerhalb des Bildschirms liegen
#         adjusted_x = max(primary_monitor.x, min(adjusted_x, primary_monitor.x + primary_monitor.width))
#         adjusted_y = max(primary_monitor.y, min(adjusted_y, primary_monitor.y + primary_monitor.height))
#         pyautogui.moveTo(adjusted_x, adjusted_y)
#     else:
#         print("No primary monitor found; cannot move cursor.")

# # Beispiel für die Verwendung dieser Funktion
# move_cursor_within_primary(500, 300)  # Bewege den Cursor zu einer bestimmten Position auf dem Hauptbildschirm
