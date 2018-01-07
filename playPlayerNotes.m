function playPlayerNotes()
    notes = dlmread('Python/WriteDir/playerNotes.txt','\t',1,0);
    times = notes(:,1);
    freqs = notes(:,2);

    times = times - times(1);
    Fs = 20000;

    tim = 1:1/Fs:(times(end)+0.5);
    y = zeros(size(tim));
    for ii = 1:numel(tim)
        t = tim(ii);

        jj = sum(times < t);
        y(ii) = sin(freqs(jj)*2*pi*t);
    end

    soundsc(y,Fs)
    audiowrite('Python/WriteDir/playerNotes.wav',y,Fs)
end