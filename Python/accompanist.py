import threading
import Queue
import numpy as np
from scipy.io import wavfile

from input_audio_thread import input_audio_thread
from processing_thread import processing_thread
from playback_thread import playback_thread

# Main accompanist driving code.
def accompanist():
    input_audio = Queue.Queue()
    rate, data = wavfile.read('../SongLibrary/Test2.wav')
    player_track = data[:,0]
    # rate, data = wavfile.read('../SongLibrary/Test2.wav')
    accompaniment_track = data[:,0]
    update_queue = Queue.Queue()

    input_thread = FuncThread(input_audio_thread, input_audio)
    process_thread = FuncThread(processing_thread, input_audio, player_track, accompaniment_track, update_queue)
    play_thread = FuncThread(playback_thread, accompaniment_track, update_queue)

    input_thread.start()
    process_thread.start()
    play_thread.start()


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