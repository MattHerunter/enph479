import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Plotting for debugging
plotting = False

# Load song from wav file
fs, song = wavfile.read('../SongLibrary/majorScaleSingle.wav')

# Check for stereo and discard if present (shouldn't happen if using preprocessSong.m)
if song.ndim is 2:
    song = song[:, 0]

abs_song = np.abs(song)
song_max = np.iinfo(song.dtype).max
song_normalized = song.astype(float) / song_max

# Load preprocessed stuff
chunks = np.loadtxt('WriteDir/playerNotes.txt', delimiter='\t', skiprows=1)
times = chunks[:, 0]
freqs = chunks[:, 1]


for note in range(freqs.size-1):
    # FFT window
    window_start = int(times[note]*fs)
    window_end = int((times[note] + (times[note + 1] - times[note])/5)*fs)

    # Get dominant frequency of note
    song_chunk = song[window_start:window_end]
    abs_song_chunk = np.abs(song_chunk)
    fft_song_chunk = np.fft.fft(song_chunk - np.mean(song_chunk))
    mag_fft_song_chunk = np.abs(fft_song_chunk)

    # Frequency vector
    freq_song_chunk = np.fft.fftfreq(fft_song_chunk.size, 1.0/fs)

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

        if plotting:
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

    print("Python Frequency: " + str(note_freq))
    print("MATLAB Frequency: " + str(freqs[note]))

    if plotting:
        plt.clf()
        plt.subplot(311)
        plot_time = np.arange(float(song_chunk.size)) / fs
        plt.plot(plot_time, abs_song_chunk, '-b', label='Raw Signal')
        plt.ylabel('Signal Amplitude')
        plt.xlabel('Time (s)')
        plt.legend()

        plt.subplot(312)
        plt.plot(freq_song_chunk, mag_fft_song_chunk, '-b', freq_song_chunk[note_freq_idx], mag_fft_song_chunk[note_freq_idx], '*r')
        plt.xlim([0, 5000])
        plt.ylabel('FFT Amplitude')
        plt.xlabel('Frequency (Hz)')
        # plt.legend()

        plt.subplot(313)
        plot_time = np.arange(float(abs_song.size)) / fs
        plt.plot(plot_time, abs_song, '-b', label='Entire Song')
        plot_time = np.arange(float(song_chunk.size)) / fs + float(window_start) / fs
        plt.plot(plot_time, abs_song_chunk, '-r', label='Current Window')
        plt.ylabel('Signal Amplitude')
        plt.xlabel('Time (s)')
        plt.legend()

        plt.tight_layout()
        plt.show()
