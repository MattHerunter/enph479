# Import for multithreading
import threading

import numpy as np
import time

def processing_thread(input_audio, player_track, accompaniment_track, update_queue):
    while True:
        data = input_audio.get()

        time.sleep(5.0)

        update = OutputUpdate(0.5,0.5)
        update_queue.put(update)


class OutputUpdate:
    def __init__(self, position, tempo):
        self.position = position
        self.tempo = tempo