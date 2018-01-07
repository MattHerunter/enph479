% Use magic to synchronize the tempo in track 2 to track 1
function [out1,out2] = synchronizeNew2(song1,Fs1,song2,Fs2,writeDir,plotting)
    time1 = (1:numel(song1))/Fs1;
    time2 = (1:numel(song2))/Fs2;
    
    % Identify song beats based on volume
    notes1 = identifySongNotes(song1,Fs1,plotting);
    beat1 = notes1(:,1);
    mag1 = notes1(:,3);
    notes2 = identifySongNotes(song2,Fs2,plotting);
    beat2 = notes2(:,1);
    mag2 = notes2(:,3);
    
    % Match beats in one song to the other
    [pair1, pair2] = matchBeatsLinear(beat1,beat2,mag1,mag2,plotting);
    
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
    
    % Normalize output data to fit in [-1,1)
    out1 = normalizeAudio(out1);
    out2 = normalizeAudio(out2);
    
    %soundsc(out1+out2,Fs1)
    % Write the synchronized tracks to file (Python prefers readin wav
    % files)
    %audiowrite('MatchTests/synchronize_out.wav',out1+out2,Fs1);
    audiowrite([writeDir '/song1_Synchronized.wav'],out1,Fs1);
    audiowrite([writeDir '/song2_Synchronized.wav'],out2,Fs2);
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

function out = normalizeAudio(a)
    out = a - min(a);
    out = out./max(out) * 1.999;
    out = out - 1;
end