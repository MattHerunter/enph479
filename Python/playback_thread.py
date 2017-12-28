# Import for multithreading
import threading

import pv
import pyaudio
import numpy as np

def playback_thread(accompaniment_track, update_queue):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    audio = pyaudio.PyAudio()
    # start Playing
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True)

    pvoc = pv.PhaseVocoder()

    while True:
        print("ass")
        update = update_queue.get()

        position = update.position
        position = int(update.position * len(accompaniment_track))
        tempo = update.tempo

        data = pvoc.speedx(accompaniment_track[position:-1], tempo)
        strdata = data.tostring()

        stream.write(strdata)


class OutputUpdate:
    def __init__(self, position, tempo):
        self.position = position
        self.tempo = tempo