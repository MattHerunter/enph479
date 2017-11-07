function songFilt = fftFilt(song,Fs,cutOffFreq)
    % Abs the song for envelope
    [freq,~,fftSong] = fftMag(abs(song),Fs);
    idx = freq <= cutOffFreq | freq >= freq(end) - cutOffFreq;
    songFilt = real(ifft(fftSong.*idx));
end