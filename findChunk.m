function betterSong = findChunk(chunk,song,Fs)
    PLOTTING = false;
    Fc = 5;
    numFreqs = 50;
    song = song(1:end-mod(numel(song),Fs/Fc));
    Nc = numel(song)*Fc/Fs;
    Lc = Fs/Fc;
    chunks = reshape(song,[Lc, Nc]);
    chunkID = zeros(numFreqs, Nc, 2);
    
    scum = [];
    fftc = 0;
    betterSong = [];
    for jj = 1:Nc
        chunk = chunks(:,jj);
        %soundsc(chunk,Fs);
        fftcl = fftc;
        fftc = abs(fft(chunk));
        F = (0:Lc-1)*Fc;
        F = F(1:ceil(end/2));
        fftc = fftc(2:ceil(end/2));
        idx = F>100 & F<5e3;
        fftc = fftc(idx);
        F = F(idx);
        [~,idx] = sort(fftc,'descend');
        idx(idx==1)=[];
        idx(idx==numel(fftc))=[];
        idx = idx(1:numFreqs);
        chunkID(:,jj,1) = F(idx);
        chunkID(:,jj,2) = fftc(idx);
        
        idx = idx((fftc(idx) > fftc(idx-1)) & (fftc(idx) > fftc(idx+1)));
        if(PLOTTING)
            subplot(2,1,1);
            plot(F,fftc,'-k',F(idx),fftc(idx),'or');
            subplot(2,1,2);
            plot(F,fftc-fftcl,'-k');
            drawnow;
        end
        scum=[scum fftc];
        x = (1:numel(chunk))./Fs;
        y = 0*x;
        for ii=idx'
            y = y + sin(2*pi*F(ii)*x)*fftc(ii);
        end
        betterSong = [betterSong y];
    end
    
    %betterSong = betterSong.*(sin(pi*Fc*(1:numel(betterSong))/Fs)).^2;
    %betterSong = [betterSong 0*(1:Lc/2)]+[0*(1:Lc/2) betterSong];
    
    %soundsc((betterSong),Fs);
end

