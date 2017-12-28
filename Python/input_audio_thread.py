# Import for multithreading
import threading

import pyaudio

def input_audio_thread(input_audio):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 256

    audio = pyaudio.PyAudio()
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        input_audio.put(data)