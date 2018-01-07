import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from time import time


def detect_notes(song_chunk, Fs, filter_b, filter_a, zi, note_detected, note_time, test_dict):

    # Algorithm Settings (these should be the same or similar to the values found in identifySongNotes.m)
    MIN_NOTE_LEN = 0.12
    DIFF_TOL = 4.8

    # Absolute value of song
    abs_song_chunk = np.abs(song_chunk)

    # Filter out higher frequencies
    abs_song_chunk_filt, zi = signal.lfilter(filter_b, filter_a, abs_song_chunk, zi=zi)
    # Halfway point used as zi for next chunk (since shifted by half)
    zi = abs_song_chunk_filt[int(abs_song_chunk_filt.size/2)]

    # Plotting for debugging/development only
    if test_dict['plotting']:
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
        plt.plot(plot_time, np.diff(abs_song_chunk_filt)*Fs, '-b', label='Derivative of Filtered Signal')
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

        plt.clf()
        plot_time = np.arange(float(song_chunk.size)) / Fs
        plt.plot(plot_time, abs_song_chunk, '-b', linewidth=2.0, label='Raw Signal')
        plt.plot(plot_time, abs_song_chunk_filt, '-r', linewidth=2.0, label='Filtered Signal')
        plt.ylabel('Signal Amplitude')
        plt.xlabel('Time (s)')
        plt.title('Comparison of Filtered and Unfiltered Signals')
        plt.legend()
        plt.show()

    # If no note has been detected,
    # search for one
    note_freq = -1
    if not note_detected:

        rising_edges = np.diff(abs_song_chunk_filt)*Fs >= DIFF_TOL

        # See if any values in the difference are above the specified tolerance
        note_idx = np.nonzero(rising_edges)[0]

        # If yes, and past the halfway point, extract the frequency
        if note_idx.size >= 1 and note_idx[0] <= rising_edges.size/2:
            note_detected = True

            # Get first note index
            note_idx = note_idx[0]
            note_time = time()

            # Get dominant frequency of note
            song_chunk_trim = song_chunk[note_idx:]
            fft_song_chunk = np.fft.fft(song_chunk_trim - np.mean(song_chunk_trim))
            mag_fft_song_chunk = np.abs(fft_song_chunk)

            # Frequency vector
            freq_song_chunk = np.fft.fftfreq(fft_song_chunk.size, 1.0/Fs)

            # Cut in half
            freq_song_chunk = freq_song_chunk[0:freq_song_chunk.size/2]
            mag_fft_song_chunk = mag_fft_song_chunk[0:mag_fft_song_chunk.size/2]

            # Get maximum frequency in the FFT
            note_freq_idx = np.argmax(mag_fft_song_chunk)
            note_freq = freq_song_chunk[note_freq_idx]

            # Attempt to correct for harmonics (sometimes the first harmonic has a higher peak than the base harmonic)
            base_harmonic = False
            harmonic_window_width = int(np.ceil(50 / np.diff(freq_song_chunk)[0]))  # 5Hz

            original_peak_mag = mag_fft_song_chunk[note_freq_idx]
            harmonic_ratio_threshold = 0.3

            while not base_harmonic:
                harmonic_window_start = int(max(note_freq_idx / 2 - harmonic_window_width / 2, 0))
                harmonic_window_end = int(min(harmonic_window_start + harmonic_window_width, mag_fft_song_chunk.size))

                mag_fft_harmonic = mag_fft_song_chunk[harmonic_window_start:harmonic_window_end]
                freq_harmonic = freq_song_chunk[harmonic_window_start:harmonic_window_end]

                harmonic_freq_idx = np.argmax(mag_fft_harmonic) + harmonic_window_start
                harmonic_ratio = mag_fft_song_chunk[harmonic_freq_idx] / original_peak_mag

                if test_dict['plotting']:
                    plt.clf()
                    plt.plot(freq_song_chunk, mag_fft_song_chunk, '-b', label='Entire FFT')
                    plt.plot(freq_harmonic, mag_fft_harmonic, '-r', label='Harmonic Search Window')
                    plt.ylabel('Signal Amplitude')
                    plt.xlabel('Time (s)')
                    plt.xlim([0, 5000])
                    plt.legend()

                if harmonic_ratio >= harmonic_ratio_threshold:
                    note_freq_idx = harmonic_freq_idx
                else:
                    base_harmonic = True

            # # Attempt to correct for harmonics (sometimes the first harmonic has a higher peak than the base harmonic)
            # base_harmonic = False
            # harmonic_window_width = int(np.ceil(5/np.diff(freq_song_chunk)[0]))  # 5Hz
            # while not base_harmonic:
            #     harmonic_window_start = int(max(note_freq_idx/2 - harmonic_window_width, 0))
            #     harmonic_window_end = int(min(harmonic_window_start + harmonic_window_width, mag_fft_song_chunk.size))
            #     harmonic_freq_idx = np.argmax(mag_fft_song_chunk[harmonic_window_start:harmonic_window_end]) + harmonic_window_start
            #
            #     if mag_fft_song_chunk[harmonic_freq_idx] >= 0.85*mag_fft_song_chunk[note_freq_idx]:
            #         note_freq_idx = harmonic_freq_idx
            #     else:
            #         base_harmonic = True

            print('time: ' + str(test_dict['time']) + ', freq: ' + str(note_freq))
            if test_dict['plotting']:
                plt.clf()
                plt.plot(freq_song_chunk, mag_fft_song_chunk, '-b', freq_song_chunk[note_freq_idx], mag_fft_song_chunk[note_freq_idx], '*r')
                plt.xlim([0, 5000])
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

# UNUSED FOR NOW
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