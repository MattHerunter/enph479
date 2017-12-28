function [out1,out2] = synchronize(Fs,time1,time2,song1,song2,beat1,beat2)
    %beat1 = [beat1(1) beat1(end)];
    %beat2 = [beat2(1) beat2(end)];
    
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
    
    %[out1,out2]=pad(song1,song2);
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