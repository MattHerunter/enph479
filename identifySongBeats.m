function beats = identifySongBeats(Fs,time,song)
    % Plot Settings
    alw = 0.75;    % AxesLineWidth
    fsz = 22;      % Fontsize
    lw = 1.1;      % LineWidth
    msz = 8;       % MarkerSize    

    % Algorithm Settings
    MIN_NOTE_LEN = 0.12;
    CUTOFF_FREQ = 30;
    DIFF_TOL = 1e-4;
    MAG_TOL = 600;
    MIN_FREQ_SPACING = 50;
    
    % Get minNoteIdx
    S2IDX = numel(time)/time(end);
    minNoteIdx = round(MIN_NOTE_LEN*S2IDX);
    
    % Filter out higher frequencies
    songFftFilt = fftFilt(abs(song),Fs,CUTOFF_FREQ);
    
    %envelope(song,Fs/100,'peak')
    %pause
    
    % Get rising edges of signal
    idx = risingEdges(songFftFilt,DIFF_TOL,minNoteIdx);
    
    % Plot of rising edge locations
    fftPlot = figure;
    set(gca, 'FontSize', fsz, 'LineWidth', alw); %<- Set properties
    figure(fftPlot);
    plot(time(idx),songFftFilt(idx),'*r',time,songFftFilt,'-k','linewidth',lw);
    legend('Derivative of Envelope');
    xlabel('Time (s)');
    ylabel('Amplitude');
    title(['Cut-off Frequency = ' num2str(CUTOFF_FREQ) ' Hz']);
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

function idx = risingEdges(x,tol,spacing)
    % Diff and diff shifted forward one
    dx = diff(x);
    dxp = [0;dx(1:end-1)];
    
    % Idx of rising edges
    idx = find(dx >= tol & dxp < tol);
    
    % Removes duplicates
    dupIdx = find(diff(idx) < spacing)+1;
    idx(dupIdx) = [];
end