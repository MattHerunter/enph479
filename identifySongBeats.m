function [beats, mag] = identifySongBeats(Fs,time,song,plotting)
    % Plot Settings
    alw = 0.75;    % AxesLineWidth
    fsz = 22;      % Fontsize
    lw = 1.1;      % LineWidth
    
    % Algorithm Settings
    MIN_NOTE_LEN = 0.12;
    CUTOFF_FREQ = 30;
    DIFF_TOL = 5e-5;
    
    % Get minNoteIdx
    S2IDX = numel(time)/time(end);
    minNoteIdx = round(MIN_NOTE_LEN*S2IDX);
    
    % Filter out higher frequencies
    songFftFilt = fftFilt(abs(song),Fs,CUTOFF_FREQ);
    
    % Get rising edges of signal
    [idx, mag] = risingEdges(songFftFilt,DIFF_TOL,minNoteIdx);
    
    % Plot of rising edge locations
    if plotting
        fftPlot = figure;
        set(gca, 'FontSize', fsz, 'LineWidth', alw); %<- Set properties
        figure(fftPlot);
        plot(time(idx),songFftFilt(idx),'*r',time,songFftFilt,'-k','linewidth',lw);
        legend('Derivative of Envelope');
        xlabel('Time (s)');
        ylabel('Amplitude');
        title(['Cut-off Frequency = ' num2str(CUTOFF_FREQ) ' Hz']);
    end
    beats = time(idx);
end

function [idx, mag] = risingEdges(x,tol,spacing)
    % Diff and diff shifted forward one
    dx = diff(x);
    dxp = [0;dx(1:end-1)];
    
    % Idx of rising edges
    idx = find(dx >= tol & dxp < tol);
    mag = zeros(size(idx));
    for ii = 1:numel(idx)
        id = idx(ii);
        while x(id+1) > x(id)
            id = id+1;
        end
        mag(ii) = x(id);
    end
    
    % Removes duplicates
    dupIdx = find(diff(idx) < spacing)+1;
    idx(dupIdx) = [];
end