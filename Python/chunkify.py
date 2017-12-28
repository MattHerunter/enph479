import numpy as np

def chunkify(song):
    MIN_CHUNK_LENGTH = 1
    SONG_LENGTH = song.shape[0]
    MIN_UNIQUENESS_TOL = 0

    # First possible chunk
    chunkStart = 0
    chunkEnd = chunkStart + MIN_CHUNK_LENGTH - 1
    numFoundChunks = 0
    chunkUnique = False

    # Allocate memory for arrays of unknown size
    chunks = np.zeros(0)

    while chunkEnd <= SONG_LENGTH:
        if chunkEnd < SONG_LENGTH:
            # Get the minimum uniqueness for the current chunk
            chunkUnique = checkChunk(song, chunkStart, chunkEnd, MIN_UNIQUENESS_TOL)

        if chunkUnique or chunkEnd is SONG_LENGTH:
            # Store found chunk
            numFoundChunks += 1
            if chunks.size is 0:
                chunks = np.array([[chunkStart, chunkEnd]])
            else:
                chunks = np.append(chunks, [[chunkStart, chunkEnd]], axis=0)

            #chunks = [chunks;[chunkStart chunkEnd]];
            # Begin search for next chunk
            chunkStart = chunkEnd + 1
            chunkEnd = chunkStart + MIN_CHUNK_LENGTH - 1

        else:
            # Increase the length if not unique enough
            chunkEnd += 1

    print('Broke signal')
    print(song)
    print(' into chunks:')
    #for jj = 1:size(chunks, 1)
    for jj in range(chunks.shape[0]):
        print('Chunk ' + str(jj))
        print(song[chunks[jj][0]:chunks[jj][1]+1, :])

    return chunks


def checkChunk(song, chunkStart, chunkEnd, MIN_UNIQUENESS_TOL):
    chunk = song[chunkStart:chunkEnd+1, :]
    chunkLength = chunkEnd - chunkStart + 1
    chunkUnique = True
    jj = 0
    while chunkUnique and (jj < song.shape[0] - chunkLength + 1):
        sChunkStart = jj
        sChunkEnd = sChunkStart + chunkLength - 1
        sChunk = song[sChunkStart:sChunkEnd+1, :]
        chunkDiff = sChunk - chunk
        chunkUniqueness = np.sum(chunkDiff**2)**0.5
        if (chunkUniqueness <= MIN_UNIQUENESS_TOL) and sChunkStart is not chunkStart and sChunkEnd is not chunkEnd:
            chunkUnique = False
        jj += 1
    return chunkUnique