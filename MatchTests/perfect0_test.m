[songL,Fs] = audioread('MatchTests/Perfect0_L.wav');
perfectL = songL(:,1);
[songR,Fs] = audioread('MatchTests/Perfect0_R.wav');
perfectR = songR(:,1);

synchronizeNew(Fs,perfectL,perfectR);
%synchronizeNew(Fs,perfectR,perfectL);