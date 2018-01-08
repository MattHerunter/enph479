import numpy as np
import matplotlib.pyplot as plt


def find_location(chunk, chunks):

    # Set all notes relative to the last note (because we'll be trying to match the most recent note in the sample to one in the song).
    # Store this in chunk_reverse and chunks_reverse.
    chunk = chunk.get()
    num_notes = 0
    for ii in range(len(chunk)):
        if chunk[ii, 0] != 0:
            num_notes += 1

    chunk_rel = chunk[chunk != 0]
    chunk_rel = np.reshape(chunk_rel, [num_notes, 2])
    #chunk_rel = np.flipud(chunk_rel)
    chunk_rel[:, 0] = chunk_rel[:, 0] - chunk_rel[-1, 0]
    chunk_rel[:, 1] = chunk_rel[:, 1] / chunk_rel[-1, 1]

    # Iterate over all notes in the song to decide which best matches the sample.
    best_cand = -1
    best_cand_qual = -float('Inf')
    qual_array = np.zeros(len(chunks))
    for ii in range(1, len(chunks)):
        # Create an array of song notes relative to the current candidate.
        chunks_rel = np.zeros(chunks.shape)
        chunks_rel[:, 0] = chunks[:, 0] - chunks[ii, 0]
        chunks_rel[:, 1] = chunks[:, 1]/chunks[ii, 1]

        # Now the notes in the sample array (chunk_reverse) should match to notes in the song array (chunks_rel).
        # Check each note in the sample array for a match in the song array above a quality threshold.
        cand_qual = 0
        for kk in range(len(chunk_rel)-1):
            note_time = chunk_rel[kk, 0]
            note_freq = chunk_rel[kk, 1]

            best_match_qual = -float('Inf')
            for jj in range(ii):
                match_time = chunks_rel[jj, 0]
                match_freq = chunks_rel[jj, 1]

                match_qual = - abs(note_time - match_time) - abs(note_freq - match_freq)
                if match_qual > best_match_qual:
                    best_match_qual = match_qual

            # Quality of current candidate (match for most recent note) increases with number and quality of matches (of previous notes).
            cand_qual = cand_qual + best_match_qual

        if cand_qual > best_cand_qual:
            best_cand_qual = cand_qual
            best_cand = ii

        qual_array[ii] = cand_qual

    #plt.plot(range(0, len(chunks)), qual_array)
    #plt.show()

    location = best_cand

    print("Location:")
    print(location)

    return location


