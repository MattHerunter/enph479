import threading
import Queue
import numpy as np
from scipy.io import wavfile

from input_audio_thread import input_audio_thread
from processing_thread import processing_thread
from playback_thread import playback_thread


# Main accompanist driving code
def accompanist():
    input_audio = Queue.Queue()
    rate, data = wavfile.read('../SongLibrary/majorScaleSingle.wav')
    # rate, data = wavfile.read('WriteDir/song1Synchronized.wav')

    # Normalize magnitude of the audio file to 1. MATLAB's audioread does the same, so this allows comparison between
    # thresholds in the two programs. Additionally, allows the same threshold to be used regardless of how many bits the
    # audio data is
    data_max = np.iinfo(data.dtype).max
    data = data.astype(float)/data_max

    # Check for stereo and discard if present (shouldn't happen if using preprocessSong.m)
    if data.ndim is 2:
        data = data[:, 0]

    player_track = data
    accompaniment_track = data
    update_queue = Queue.Queue()

    # Testing information for processing_thread
    test_dict = {'song': player_track, 'Fs': rate, 'plotting': True}

    input_thread = FuncThread(input_audio_thread, input_audio, test_dict)
    process_thread = FuncThread(processing_thread, input_audio, player_track, accompaniment_track, update_queue, test_dict)
    play_thread = FuncThread(playback_thread, accompaniment_track, update_queue)

    input_thread.start()
    process_thread.start()
    #play_thread.start()


# Implements threads that can take parameters
class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)


# This gets called when run as a script
if __name__ == '__main__':
    testing = False
    if not testing:
        accompanist()
    else:
        testing = False
