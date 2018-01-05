% Call this function before the Python routines to write the necessary
% audio/data to writeDir
function preprocessSong(playerTrackPath, accompTrackPath, writeDir)
    % Flags to control plotting for debugging purposes
    plotIdentifySongNotes = true;
    plotSynchronize = true;
    
    % Load the player's and accompanist's tracks
    [playerSong,playerFs] = audioread(playerTrackPath);
    [accompSong,accompFs] = audioread(accompTrackPath);
    
    % Discard stereo if present
    if size(playerSong,2) == 2
        playerSong = playerSong(:,1);
    end
    if size(accompSong,2) == 2
        accompSong = accompSong(:,1);
    end
    
    % Align the tempos of the two tracks and store in writeDir
    synchronizeNew2(playerSong, playerFs, accompSong, accompFs, writeDir, plotSynchronize);
    
    % Identify notes in the player track
    playerNotes = identifySongNotes(playerSong, playerFs, plotIdentifySongNotes);
    
    % Write the data to file
    fid = fopen([writeDir '/playerNotes.txt'],'w');
    fprintf(fid, 'Time (s)\tFrequency (Hz)\n');
    fprintf(fid, '%.2f\t%.2f\n', playerNotes');
end