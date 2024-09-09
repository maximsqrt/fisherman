# import pyaudio

# def list_audio_devices():
#     p = pyaudio.PyAudio()
#     # Holen Sie sich die Anzahl der verfügbaren Geräte
#     device_count = p.get_device_count()
    
#     # Durchlaufe alle verfügbaren Geräte und drucke ihre Informationen
#     for index in range(device_count):
#         device_info = p.get_device_info_by_index(index)
#         print(f"Device Index: {index}")
#         print(f"Name: {device_info.get('name')}")
#         print(f"Max Input Channels: {device_info.get('maxInputChannels')}")
#         print(f"Max Output Channels: {device_info.get('maxOutputChannels')}")
#         print("")

# if __name__ == "__main__":
#     list_audio_devices()
import pyaudio
import wave

# Parameter für PyAudio-Stream
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

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

    # Aufnahme für eine bestimmte Zeit
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stoppe und schließe den Stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Speichern der aufgenommenen Daten als WAV-Datei
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

if __name__ == "__main__":
    main()
