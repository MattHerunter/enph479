function chunks = chunkify(song)
    MIN_CHUNK_LENGTH = 1;
    MAX_CHUNK_LENGTH = size(song,1);
    MIN_UNIQUENESS_TOL = 0;
    
    % First possible chunk
    chunkStart = 1;
    chunkEnd = chunkStart + MIN_CHUNK_LENGTH - 1;
    numFoundChunks = 0;
    
    % Allocate memory for arrays of unknown size
    %chunks = nan(ceil(size(song,1)/MIN_CHUNK_LENGTH),2);
    chunks = [];
    
    while chunkEnd <= size(song,1)
        if chunkEnd < size(song,1)
            % Get the minimum uniqueness for the current chunk
            chunkUnique = checkChunk(song,chunkStart,chunkEnd,MIN_UNIQUENESS_TOL);
        end
        if chunkUnique || (chunkEnd == size(song,1))
            % Store found chunk
            numFoundChunks = numFoundChunks+1;
            chunks = [chunks;[chunkStart chunkEnd]];
            % Begin search for next chunk
            chunkStart = chunkEnd+1;
            chunkEnd  = chunkStart + MIN_CHUNK_LENGTH - 1;
            
        else
            % Increase the length if not unique enough
            chunkEnd = chunkEnd+1;
        end
    end
    
    disp('Broke signal');
    disp(num2str(song));
    disp(' into chunks:');
    for jj=1:size(chunks,1)
        disp(['Chunk ' num2str(jj)]);
        disp(song(chunks(jj,1):chunks(jj,2),:));
    end
end

function chunkUnique = checkChunk(song,chunkStart,chunkEnd,MIN_UNIQUENESS_TOL)
    chunk = song(chunkStart:chunkEnd,:);
    chunkLength = chunkEnd - chunkStart + 1;
    chunkUnique = true;
    jj = 1;
    while chunkUnique && (jj <= size(song,1) - chunkLength + 1)
        sChunkStart = jj;
        sChunkEnd = sChunkStart + chunkLength - 1;
        sChunk = song(sChunkStart:sChunkEnd,:);
        chunkDiff = sChunk - chunk;
        chunkUniqueness = sum(chunkDiff(:).^2)^0.5;
        if (chunkUniqueness <= MIN_UNIQUENESS_TOL) && all([sChunkStart;sChunkEnd] ~= [chunkStart;chunkEnd])
            chunkUnique = false;
        end
        jj = jj + 1;
    end
end