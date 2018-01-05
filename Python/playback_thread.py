import pv
import pyaudio


def playback_thread(accompaniment_track, update_queue, audio):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    #audio = pyaudio.PyAudio()

    # Detect speakers
    device_count = audio.get_device_count()
    for i in range(0, device_count):
        print("Name: " + audio.get_device_info_by_index(i)["name"])
        print("Index: " + str(audio.get_device_info_by_index(i)["index"]))
        print("\n")


    # start Playing
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True)

    pvoc = pv.PhaseVocoder()


    while True:
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