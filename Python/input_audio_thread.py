import pyaudio
import time


def input_audio_thread(input_audio, audio, test_dict):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = RATE/5
    TESTING = True

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    ii = 0
    while True:
        if TESTING:
            # Get section of song
            chunk_start = int(ii/2.*CHUNK)
            chunk_end = chunk_start + CHUNK
            data = test_dict['song'][chunk_start:chunk_end]
            input_audio.put(data)
            time.sleep(float(CHUNK)/test_dict['Fs'])
            ii += 1
        else:
            data = stream.read(CHUNK)
            input_audio.put(data)

