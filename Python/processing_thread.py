import numpy as np
from detect_notes import detect_notes
from find_location import find_location
from scipy import signal
from ringbuffer import RingBuffer


def processing_thread(input_audio, player_track, accompaniment_track, update_queue, test_dict):

    # Algorithm initial conditions
    note_detected = False
    note_time = 0
    note_freq = -1
    time = 0
    detected_notes = RingBuffer(10)
    init_zi = True

    # Heinous hack
    Fs = 44100

    # Low pass filter parameters
    filter_cutoff = 30.0
    filter_order = 4

    # Design the filter
    [filter_b, filter_a, ] = signal.bessel(filter_order, [filter_cutoff / (Fs / 2.0)], btype='low', analog=False)

    # Filter initial conditions
    zi = signal.lfilter_zi(filter_b, filter_a)

    # Load the preprocessed notes written by preprocessSong.m
    # chunks = np.array([[0.2604, 0.8972, 1.4835, 2.0877, 2.6649, 3.2505, 3.8320, 4.4837],
    #                    [241.6438, 266.6415, 270.8077, 320.8030, 358.2995, 358.2995, 404.1285, 483.2877]]).T

    chunks = np.loadtxt('WriteDir/playerNotes.txt', delimiter='\t', skiprows=1)

    # Make relative chunks (difference in time, ratio in frequency)
    rel_times = np.diff(chunks[:, 0])
    rel_freqs = chunks[1:, 1]/chunks[0:-1, 1]
    rel_chunks = np.c_[rel_times, rel_freqs]

    while True:
        # Get next chunk of data from the input_audio queue
        song_chunk = input_audio.get()

        # Initialize the filter value
        if init_zi:
            zi = zi*song_chunk[0]
            init_zi = False

        # Detect song notes
        test_dict['time'] = time
        time += float(song_chunk.size) / Fs
        id_notes_dict = detect_notes(song_chunk, Fs, filter_b, filter_a, zi, note_detected, note_time, test_dict)

        # Update some of the values from the function
        note_detected = id_notes_dict['note_detected']
        note_time_prev = note_time
        note_time = id_notes_dict['note_time']
        zi = id_notes_dict['zi']

        # If the note time has changed, a new note was detected, so updated the note_freq
        if note_time is not note_time_prev:
            note_freq_prev = note_freq
            note_freq = id_notes_dict['note_freq']

            # Need at least two note detections since we are working with relative frequencies/timings
            if note_freq_prev is not -1:
                rel_note = np.array([[note_time - note_time_prev, note_freq/note_freq_prev]])
                detected_notes.extend(rel_note)
                #print(detected_notes.get())

                # Find chunk location
                chunk_location = find_location(detected_notes, rel_chunks)

                # Set position/tempo of the update
                position = chunk_location
                update = OutputUpdate(position, 1.0)
                update_queue.put(update)


class OutputUpdate:
    def __init__(self, position, tempo):
        self.position = position
        self.tempo = tempo
