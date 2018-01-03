function [out1,out2] = synchronizeNew(Fs,song1,song2)
    time1 = (1:numel(song1))/Fs;
    time2 = (1:numel(song2))/Fs;
    
    [beat1, mag1] = identifySongBeats(Fs,time1,song1);
    [beat2, mag2] = identifySongBeats(Fs,time2,song2);
    
    [pair1, pair2] = matchBeatsLinear(beat1,beat2,mag1,mag2);
    
    beat1 = beat1(pair1);
    beat2 = beat2(pair2);
    
    out2 = [];
    for ii = 1:numel(beat1)-1
       tempo = (beat2(ii+1)-beat2(ii))/(beat1(ii+1)-beat1(ii));
       chunk = pvoc(song2(time2>beat2(ii)&time2<beat2(ii+1)),tempo,1000);
       target = sum(time1>beat1(ii)&time1<beat1(ii+1));
       if numel(chunk) < target
           chunk = [chunk;zeros(target-numel(chunk),1)];
       else
           chunk = chunk(1:target); 
       end
       out2 = [out2;chunk];
    end
    out2 = [out2;song2(time2>beat2(end))];
    out1 = song1(time1 > beat1(1));
    [out1,out2]=pad(out1,out2);
    
    soundsc(out1+out2,Fs);
    audiowrite('MatchTests/synchronize_out.wav',out1+out2,Fs);
end

function [ap,bp] = pad(a,b)
    if numel(a) < numel(b)
        bp = b;
        ap = zeros(size(b));
        ap(1:numel(a)) = a;
    else
        ap = a;
        bp = zeros(size(a));
        bp(1:numel(b)) = b;
    end
end