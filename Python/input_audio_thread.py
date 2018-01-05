import pyaudio
import time


def input_audio_thread(input_audio, audio, test_dict):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = RATE/10
    TESTING = True

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    ii = 0
    while True:
        if TESTING:
            # Get section of song
            data = test_dict['song'][ii*CHUNK:(ii+1)*CHUNK]
            input_audio.put(data)
            time.sleep(float(CHUNK)/test_dict['Fs'])
            ii += 1
        else:
            data = stream.read(CHUNK)
            input_audio.put(data)

