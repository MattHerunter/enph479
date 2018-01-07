import pv
import pyaudio
import numpy as np
import time

def playback_thread(accompaniment_track, update_queue, audio):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    # Print audio devices
    device_count = audio.get_device_count()
    for i in range(0, device_count):
        print("Name: " + audio.get_device_info_by_index(i)["name"])
        print("Index: " + str(audio.get_device_info_by_index(i)["index"]))
        print("\n")

    # Open output audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

    # Phase vocoder for tempo alignment
    pvoc = pv.PhaseVocoder()

    chunks = np.loadtxt('WriteDir/playerNotes.txt', delimiter='\t', skiprows=1)

    update = OutputUpdate(0,1)
    updateTime = time.time()
    while True:
        if not update_queue.empty():
            update = update_queue.get()
            updateTime = time.time()

        # position = int(update.position * len(accompaniment_track))
        tempo = update.tempo
        position = update.position
        currTime = time.time()
        idx = int((chunks[position, 0] + currTime-updateTime)*RATE)
        data = accompaniment_track[idx:]

        if len(data) > 0.1*RATE:
            data = data[0:int(0.1*RATE)]

        # Disabling pvoc for basic testing currently
        # data = pvoc.speedx(data, tempo)

        strdata = data.tostring()

        stream.write(strdata)


class OutputUpdate:
    def __init__(self, position, tempo):
        self.position = position
        self.tempo = tempo
