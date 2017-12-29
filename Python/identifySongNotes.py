import numpy as np
from scipy import signal
from time import time

def identifySongNotes(songChunk, Fs, filter_b, filter_a, note_detected, note_time):

    # Algorithm Settings
    MIN_NOTE_LEN = 0.12
    MIN_NOTE_IDX = MIN_NOTE_LEN * Fs
    DIFF_TOL = 4.8

    # Filter out higher frequencies
    #FILTER_CUTOFF = 30.0
    #FILTER_ORD = 4
    #filter_b, filter_a = signal.bessel(FILTER_ORD, [FILTER_CUTOFF / (Fs / 2.0)], btype='low', analog=False) # Do this outside loop
    songChunkFilt = signal.filtfilt(filter_b, filter_a, np.abs(songChunk)) # type: np.ndarray

    note_freq = 0
    #while True:
    # If no note has been detected, search for one
    if not note_detected:
        note_idx = np.nonzero(np.diff(songChunkFilt) >= DIFF_TOL)[0] # type: np.ndarray
        if note_idx.size >= 1:
            note_detected = True

            # Get first note index
            note_idx = note_idx[0]
            note_time = time()

            # Get dominant frequency of note
            fftSongChunk = np.fft.fft(songChunkFilt)
            absFftSongChunk = np.abs(fftSongChunk)
            freqSongChunk = np.fft.fftfreq(fftSongChunk.size, 1.0/Fs)

            note_freq = freqSongChunk[np.argmax(absFftSongChunk - np.mean(absFftSongChunk))]

    # Reset the flag after enough time has passed
    elif time() - note_time >= MIN_NOTE_LEN:
        note_detected = False

    return {'note_detected': note_detected, 'note_time': note_time, 'note_freq': note_freq}


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