import numpy as np
import matplotlib.pyplot as plt

def find_location(chunk, chunks):
    # TESTING
    # Preprocessed relative time/frequency pairs
    # a = np.array([[1, 2, 3, 4, 5], [1, 3, 3, 4, 5]]).T
    # chunks = a
    # Current chunk of relative time/frequency pairs
    # b = np.array([[2, 3], [3, 3]]).T
    # chunk = b
    # Array to hold mean differences

    # c = np.zeros([chunks.shape[0] - chunk.shape[0], chunks.shape[1]])
    #
    # # Subtract the chunk from the preprocessed list to get the differences
    # for ii in range(c.shape[0]):
    #     c[ii] = np.mean(np.abs(chunks[ii:ii + chunk.shape[0]] - chunk), axis=0)
    #
    # # Weights to adjust the effect of time/frequency differences
    # freqWeight = 1
    # timeWeight = 1
    #
    # # Vector combining time/frequency differences (ideally 0 for perfect match)
    # match = (timeWeight*c[:, 0] + freqWeight*c[:, 1])/(timeWeight + freqWeight)
    #
    # # Find the minimum value
    # location = np.argmin(match)
    #
    # print("FINDLOCATION INFO:")
    # print("Chunk:")
    # print(chunk)
    # print("Chunks:")
    # print(chunks)
    # print("Location: ")
    # print(location)
    #
    # return location

    # print("FINDLOCATION INFO:")
    # print("Chunk:")
    # print(chunk.get())
    # print("Chunks:")
    # print(chunks)

    # Set all notes relative to the last note (because we'll be trying to match the most recent note in the sample to one in the song).
    # Store this in chunk_reverse and chunks_reverse.
    chunk = chunk.get()
    num_notes = 0
    for ii in range(len(chunk)):
        if chunk[ii, 0] != 0:
            num_notes = num_notes + 1

    chunk_reverse = np.zeros([num_notes, 2])
    chunk_reverse[num_notes - 1, 0] = - chunk[len(chunk) - 1, 0]
    chunk_reverse[num_notes - 1, 1] = 1.0 / chunk[len(chunk) - 1, 1]
    for ii in range(1, num_notes):
        chunk_reverse[num_notes - ii - 1, 0] = chunk_reverse[num_notes - ii, 0] - chunk[len(chunk) - ii - 1, 0]
        chunk_reverse[num_notes - ii - 1, 1] = chunk_reverse[num_notes - ii, 1] / chunk[len(chunk) - ii - 1, 1]

    chunks_reverse = np.zeros([len(chunks), 2])
    chunks_reverse[len(chunks) - 1, 0] = - chunks[len(chunks) - 1, 0]
    chunks_reverse[len(chunks) - 1, 1] = 1.0 / chunks[len(chunks) - 1, 1]
    for ii in range(1, len(chunks)):
        chunks_reverse[len(chunks) - ii - 1, 0] = chunks_reverse[len(chunks) - ii, 0] - chunks[len(chunks) - ii - 1, 0]
        chunks_reverse[len(chunks) - ii - 1, 1] = chunks_reverse[len(chunks) - ii, 1] / chunks[len(chunks) - ii - 1, 1]

    # print("Chunk rev:")
    # print(chunk_reverse)
    # print("Chunks rev:")
    # print(chunks_reverse)

    # Iterate over all notes in the song to decide which best matches the sample.
    best_cand = -1
    best_cand_qual = -float('Inf')
    qual_array = np.zeros(len(chunks))
    for ii in range(1, len(chunks)):
        # Create an array of song notes relative to the current candidate.
        chunks_rel = np.zeros([ii, 2])
        for jj in range(ii):
            chunks_rel[jj, 0] = chunks_reverse[jj, 0] - chunks_reverse[ii, 0]
            chunks_rel[jj, 1] = chunks_reverse[jj, 1] / chunks_reverse[ii, 1]

        # Now the notes in the sample array (chunk_reverse) should match to notes in the song array (chunks_rel).
        # Check each note in the sample array for a match in the song array above a quality threshold.
        cand_qual = 0
        for kk in range(len(chunk_reverse)):
            note_time = chunk_reverse[kk, 0]
            note_freq = chunk_reverse[kk, 1]

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

    plt.plot(range(0,len(chunks)),qual_array)
    plt.show()

    location = best_cand

    # print("Location:")
    # print(location)

    return location


