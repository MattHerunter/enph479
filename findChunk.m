function chunkIdx = findChunk(chunk,song,Fs)
    Fc = 10;
    song = song(1:end-mod(numel(song),Fs/Fc));
    Nc = numel(song)*Fc/Fs;
    Lc = Fs/Fc;
    chunks = reshape(song,[Lc, Nc]);
    
    betterSong = [];
    for jj = 1:Nc
        chunk = chunks(:,jj);
        %sound(chunk,Fs);
        F = (0:Lc-1)*Fc;
        fftc = abs(fft(chunk));
        F = F(1:ceil(end/2));
        fftc = fftc(2:ceil(end/2));
        idx = F>100 & F<5e3;
        fftc = fftc(idx);
        F = F(idx);
        [~,idx] = sort(fftc,'descend');
        idx = idx(1:20);
        %plot(F,fftc,'-k',F(idx),fftc(idx),'or');
        %drawnow;
        
        x = (1:numel(chunk))./Fs;
        y = 0*x;
        for ii=idx'
            y = y + sin(2*pi*F(ii)*x)*fftc(ii);
        end
        betterSong = [betterSong y];
        
        %pause(0.1);
    end
    
    sound(betterSong,Fs);
end

