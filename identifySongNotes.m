function notes = identifySongNotes()
    % Plot Settings
    alw = 0.75;    % AxesLineWidth
    fsz = 22;      % Fontsize
    lw = 1.5;      % LineWidth
    msz = 12;       % MarkerSize
    
    % Algorithm Settings
    PLOTTING = 1;
    MIN_NOTE_LEN = 0.12;
    CUTOFF_FREQ = 30;
    DIFF_TOL = 4.8;
    MAG_TOL = 592;
    MIN_FREQ_SPACING = 50;
    SONG_FILE = 'majorScaleSingle.wav';
    %SONG_FILE = 'matchTest0_R.m4a';
    
    % Load song, discard stereo if present
    [song,Fs] = audioread(SONG_FILE);
    song = song(:,1);
    t = (1:numel(song))/Fs;
    S2IDX = numel(t)/t(end);
    minNoteIdx = round(MIN_NOTE_LEN*S2IDX);
    
    % Filter out higher frequencies
    songFftFilt = fftFilt(abs(song),Fs,CUTOFF_FREQ);
    
    % Get rising edges of signal
    idx = risingEdges(songFftFilt,Fs,DIFF_TOL,minNoteIdx);
    
    % Plot of rising edge locations
    if PLOTTING
        fftPlot = figure;
        figure(fftPlot);
        plot(t,songFftFilt,'-k',t(idx),songFftFilt(idx),'xr','linewidth',lw,'MarkerSize',msz);
        legend('Volume of Signal','Note Detections');
        xlabel('Time (s)');
        ylabel('Amplitude');
        title('Note Detection on Major Scale');
        set(gca, 'FontSize', fsz, 'LineWidth', alw); %<- Set properties
        A = axis;
        axis([0 5 A(3) A(4)]) 
        pbaspect([1 1 1]);
        pause;
    end
    
    notes(:,1) = t(idx);
    
    % Find the frequencies of each peak
    for ii = 1:numel(idx)
        [freq, mag] = fftMag(song((idx(ii)-minNoteIdx):(idx(ii)+minNoteIdx)),Fs);
        noteIdx = 1:ceil(numel(freq)/2);
        freq = freq(noteIdx);
        mag = mag(noteIdx);
        
        pkIdxs = peakIdxs(mag,MAG_TOL,MIN_FREQ_SPACING);
        notes(ii,2) = freq(pkIdxs(1));
        
        % Plot frequencies
        if PLOTTING
            plot(freq(pkIdxs),mag(pkIdxs),'*r',freq,mag,'-k');
            pause
        end
    end
    
end

% Find peaks of x above tol atleast spacing apart (need something better
% for dealing with dups)
function idx = peakIdxs(x,tol,spacing)
    % x vector shifted forward and backward one index
    xn = [x(2:end);0];
    xp = [0;x(1:end-1)];
    
    % Peaks above tol
    idx = find(x >= xp & x >= xn & x >= tol);
    
    % Not far enough apart, likely duplicate peaks
    dups = find(diff(idx) < spacing);
    
    dupIdx = [];
    % Remove lower peak
    for jj=1:numel(dups)
        if x(idx(dups(jj))) >= x(idx(dups(jj)+1))
            dupIdx = [dupIdx;dups(jj)+1];
        else
            dupIdx = [dupIdx;dups(jj)];
        end
    end
    
    idx(dupIdx)=[];
end

function idx = risingEdges(x,Fs,tol,spacing)
    % Diff and diff shifted forward one
    dx = diff(x)*Fs;
    dxp = [0;dx(1:end-1)];
    
    % Idx of rising edges
    idx = find(dx >= tol & dxp < tol);
    %idx = find(dx >= tol);
    
    % Removes duplicates
    dupIdx = find(diff(idx) < spacing)+1;
    idx(dupIdx) = [];
end