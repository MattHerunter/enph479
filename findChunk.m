function chunkID = findChunk(chunk,song,Fs)
    PLOTTING = true;
    Fc = 10;
    numFreqs = 20;
    song = song(1:end-mod(numel(song),Fs/Fc));
    Nc = numel(song)*Fc/Fs;
    Lc = Fs/Fc;
    chunks = reshape(song,[Lc, Nc]);
    chunkID = zeros(numFreqs, Nc, 2);
    
    betterSong = [];
    for jj = 1:Nc
        chunk = chunks(:,jj);
        F = (0:Lc-1)*Fc;
        fftc = abs(fft(chunk));
        F = F(1:ceil(end/2));
        fftc = fftc(2:ceil(end/2));
        idx = F>100 & F<5e3;
        fftc = fftc(idx);
        F = F(idx);
        [~,idx] = sort(fftc,'descend');
        idx(idx==1)=[];
        idx = idx(1:numFreqs);
        chunkID(:,jj,1) = F(idx);
        chunkID(:,jj,2) = fftc(idx);
        
        idx = idx((fftc(idx) > fftc(idx-1)) & (fftc(idx) > fftc(idx+1)));
        if(PLOTTING)
            plot(F,fftc,'-k',F(idx),fftc(idx),'or');
            drawnow;
        end
        
        x = (1:numel(chunk))./Fs;
        y = 0*x;
        for ii=idx'
            y = y + sin(2*pi*F(ii)*x)*fftc(ii);
        end
        betterSong = [betterSong y];
    end
    
    sound(betterSong,Fs);
end

