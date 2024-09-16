# test_logging.py
import logging
import os

# Definiere den Pfad für die Log-Datei
log_filename = 'test_app.log'
log_path = os.path.join(os.getcwd(), log_filename)

# Konfiguriere das Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_path,
    filemode='w'  # 'w' überschreibt die Datei bei jedem Start des Skripts
)

# Log-Nachricht ausgeben
logging.debug("Test-Nachricht: Logging ist konfiguriert und aktiv.")

# Ausführen und überprüfen
print(f"Logging in: {log_path}")
