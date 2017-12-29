from scipy.io import wavfile
import pyaudio
import time
import numpy as np
import matplotlib.pyplot as plt


def input_audio_thread(input_audio):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 256*5
    TESTING = True

    audio = pyaudio.PyAudio()
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    if TESTING:
        rate, test_data = wavfile.read('../SongLibrary/majorScaleSingle.wav')
        test_data = test_data[:, 0]
        ii = 0
        # Plot song
        #plt.plot(np.arange(float(test_data.size))/RATE, test_data)
        #plt.show()
    while True:
        if TESTING:
            # Get section of song
            data = test_data[ii*CHUNK:(ii+1)*CHUNK]
            # Show on plot
            # plt.clf()
            # plt.plot(np.arange(float(test_data.size)) / RATE, test_data)
            # plt.plot((np.arange(float(CHUNK))+ii*CHUNK) / RATE, data)
            # plt.show()

            input_audio.put(data)
            time.sleep(float(CHUNK)/RATE)
            ii += 1
        else:
            data = stream.read(CHUNK)
            input_audio.put(data)

