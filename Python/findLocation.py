import numpy as np

def findLocation(chunk, chunks):
    # TESTING
    # Preprocessed relative time/frequency pairs
    # a = np.array([[1, 2, 3, 4, 5], [1, 3, 3, 4, 5]]).T
    # chunks = a
    # Current chunk of relative time/frequency pairs
    # b = np.array([[2, 3], [3, 3]]).T
    # chunk = b
    # Array to hold mean differences


    c = np.zeros([chunks.shape[0] - chunk.shape[0], chunks.shape[1]])

    # Subtract the chunk from the preprocessed list to get the differences
    for ii in range(c.shape[0]):
        c[ii] = np.mean(np.abs(chunks[ii:ii + chunk.shape[0]] - chunk), axis=0)

    # Weights to adjust the effect of time/frequency differences
    freqWeight = 1
    timeWeight = 1

    # Vector combining time/frequency differences (ideally 0 for perfect match)
    match = (timeWeight*c[:, 0] + freqWeight*c[:, 1])/(timeWeight + freqWeight)

    # Find the minimum value
    location = np.argmin(match)
    print(location)

    return location


