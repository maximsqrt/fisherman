import pyaudio
import numpy as np
from scipy.signal import correlate
from pydub import AudioSegment
import time

# Parameter für PyAudio-Stream
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 1024

# Lade den Sound, der abgespielt wird, wenn ein Fisch anbeißt
bite_sound_path = '/Users/magnus/Documents/fishersfritz/bitesound.m4a'
bite_sound = AudioSegment.from_file(bite_sound_path)

def compare_sounds(sound1, sound2):
    # Konvertiere AudioSegment in numpy Array
    sound1_data = np.array(sound1.get_array_of_samples())
    sound2_data = np.array(sound2.get_array_of_samples())

    # Berechne Kreuzkorrelation
    correlation = np.max(correlate(sound1_data, sound2_data, mode='valid'))
    return correlation

def main():
    p = pyaudio.PyAudio()

    # Open PyAudio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=1,  # BlackHole 2ch
                    frames_per_buffer=CHUNK)

    print("Start recording...")

    frames = []
    record_seconds = 5  # Aufnahmezeit in Sekunden

    # Aufnahme für eine bestimmte Zeit
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stoppe und schließe den Stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Speichern der aufgenommenen Daten als WAV-Datei
    recorded_sound = AudioSegment(
        b''.join(frames),
        sample_width=2,
        frame_rate=RATE,
        channels=CHANNELS
    )

    # Vergleiche den aufgenommenen Sound mit dem gespeicherten Sound
    correlation = compare_sounds(bite_sound, recorded_sound)

    # Normalisiere die Korrelation auf einen Bereich von 0 bis 1
    max_correlation = len(recorded_sound.get_array_of_samples()) - len(bite_sound.get_array_of_samples()) + 1
    normalized_correlation = correlation / max_correlation

    # Berechne die Übereinstimmung in Prozent
    match_percentage = normalized_correlation * 100
    print(f"Match Percentage: {match_percentage:.2f}%")

if __name__ == "__main__":
    main()
