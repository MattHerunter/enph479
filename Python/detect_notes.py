import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from time import time


def detect_notes(song_chunk, Fs, filter_b, filter_a, zi, note_detected, note_time, test_dict):

    # Algorithm Settings
    MIN_NOTE_LEN = 0.12
    DIFF_TOL = 4.8
    PLOTTING = True

    abs_song_chunk = np.abs(song_chunk)

    # Filter out higher frequencies
    abs_song_chunk_filt, zi = signal.lfilter(filter_b, filter_a, abs_song_chunk, zi=zi)

    if PLOTTING:
        plt.clf()
        plt.subplot(311)
        plot_time = np.arange(float(song_chunk.size))/Fs
        plt.plot(plot_time, abs_song_chunk, '-b', label='Raw Signal')
        plt.plot(plot_time, abs_song_chunk_filt, '-r', label='Filtered Signal')
        plt.ylabel('Signal Amplitude')
        plt.xlabel('Time (s)')
        plt.legend()

        plt.subplot(312)
        plot_time = np.arange(float(song_chunk.size - 1))/Fs
        plt.plot(plot_time, np.diff(abs_song_chunk_filt), '-b', label='Derivative of Filtered Signal')
        plt.plot(plot_time, np.ones(plot_time.shape)*DIFF_TOL, '-r', label='Detection Threshold')
        plt.ylabel('Signal Amplitude')
        plt.xlabel('Time (s)')
        plt.legend()

        plt.subplot(313)
        song = np.abs(test_dict['song'])
        plot_time = np.arange(float(song.size)) / Fs
        plt.plot(plot_time, song, '-b', label='Entire Song')
        plot_time = np.arange(float(song_chunk.size)) / Fs + test_dict['time']
        plt.plot(plot_time, abs_song_chunk, '-r', label='Current Window')
        plt.ylabel('Signal Amplitude')
        plt.xlabel('Time (s)')
        plt.legend()

        plt.tight_layout()
        plt.show()

    note_freq = -1
    # If no note has been detected, search for one
    if not note_detected:
        note_idx = np.nonzero(np.diff(abs_song_chunk_filt) >= DIFF_TOL)[0]  # type: np.ndarray
        if note_idx.size >= 1:
            note_detected = True

            # Get first note index
            note_idx = note_idx[0]
            note_time = time()

            # Get dominant frequency of note
            fft_song_chunk = np.fft.fft(song_chunk - np.mean(song_chunk))
            mag_fft_song_chunk = np.abs(fft_song_chunk)

            # Frequency vector
            freq_song_chunk = np.fft.fftfreq(fft_song_chunk.size, 1.0/Fs)

            # Cut in half
            freq_song_chunk = freq_song_chunk[0:freq_song_chunk.size/2]
            mag_fft_song_chunk = mag_fft_song_chunk[0:mag_fft_song_chunk.size/2]

            # Get max and attempt to correct for harmonics
            note_freq_idx = np.argmax(mag_fft_song_chunk)
            note_freq = freq_song_chunk[note_freq_idx]
            base_harmonic = False
            harmonic_window_width = np.ceil(float(mag_fft_song_chunk.size)/20)
            while not base_harmonic:
                note_freq_harmonic_idx = np.argmax(mag_fft_song_chunk[:])
                note_freq_idx = np.argmax(mag_fft_song_chunk)
                note_freq = freq_song_chunk[note_freq_idx]

            print('time: ' + str(test_dict['time']) + ', freq: ' + str(note_freq))
            if PLOTTING and False:
                plt.clf()
                plt.plot(freq_song_chunk, mag_fft_song_chunk, '-b', freq_song_chunk[note_freq_idx], mag_fft_song_chunk[note_freq_idx], '*r')
                plt.show()
            
    # Reset the flag after enough time has passed
    elif time() - note_time >= MIN_NOTE_LEN:
        note_detected = False

    return {'note_detected': note_detected, 'note_time': note_time, 'note_freq': note_freq, 'zi': zi}


# UNUSED FOR NOW
# Find peaks of x above tol atleast spacing apart(need something better
# for dealing with dups)
def peakIdxs(x, tol, spacing):
    # x vector shifted forward and backward one index
    xn = np.c_[x[2:-1],0]
    xp = np.c_[0,x[:-2]]

    # Peaks above tol
    idx = np.nonzero(np.logical_and(np.logical_and(x >= xp, x >= xn),x >= tol))[0]

    # Not far enough apart, likely duplicate peaks
    dups = np.nonzero(np.diff(idx) < spacing)[0]

    dupIdx = np.array(0)
    # Remove lower peak
    for jj in range(dups):
        if x[idx[dups[jj]]] >= x[idx[dups[jj] + 1]]:
            dupIdx = np.c_[dupIdx, dups(jj) + 1]
        else:
            dupIdx = np.c_[dupIdx, dups(jj)]
    dupIdx = np.delete(dupIdx,0)
    idx = np.delete(idx,dupIdx)
    return idx


def detectRisingEdge(x, Fs, tol, spacing):
    # Diff and diff shifted forward one
    dx = np.diff(x)*Fs
    dxp = np.c_[0,dx[:-2]]

    # Idx of rising edges
    #idx = np.nonzero(np.logical_and(dx >= tol,dxp < tol))[0]
    idx = np.nonzero(dx >= tol)[0]

    # Removes duplicates
    #dupIdx = np.nonzero(np.diff(idx) < spacing)[0] + 1
    #idx = np.delete(idx,dupIdx)
    return idx[0]