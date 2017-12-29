function [freq, mag, fftSong] = fftMag(song,Fs)
    fftSong = fft(song);
    mag = abs(fftSong);
    freq = (0:numel(mag)-1)'*Fs/numel(mag);
    %freq = freq(1:ceil(end/2));
    %mag = mag(1:ceil(end/2));
end

