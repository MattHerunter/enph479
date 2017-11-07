function beat3 = matchBeats(beat1,beat2)
    t = linspace(0,beat1(end),1000);
    
    bestq = -inf;
    bestpair1 = [];
    bestpair2 = [];
    
    maxpairs = min(numel(beat1)-2,numel(beat2)-2);
    minpairs = 3;
    bestqn = -inf*(1:maxpairs);
    for ii = 1:(2^(numel(beat2)-2)-1)
        ii
        bin2 = dec2bin(ii);
        bin2 = bin2 ~= '0';
        bin2 = [0*(1:(numel(beat2)-2-numel(bin2))) bin2];
        if (sum(bin2) > maxpairs) || (sum(bin2) < minpairs)
            continue;
        end
        pair2 = [1 find(bin2)+1 numel(beat2)];
        
        for jj = 1:(2^(numel(beat1)-2)-1)
            bin1 = dec2bin(jj);
            bin1 = bin1 ~= '0';
            bin1 = [0*(1:(numel(beat1)-2-numel(bin1))) bin1];
            if sum(bin1) ~= sum(bin2)
                continue;
            end
            pair1 = [1 find(bin1)+1 numel(beat1)];
            
            s = spline(beat2(pair2),beat1(pair1),t);
            q = matchQuality(s,pair1,pair2);
            if q > bestq
                bestq = q;
                bestpair1 = pair1;
                bestpair2 = pair2;
            end
            if q > bestqn(sum(bin1))
               bestqn(sum(bin1)) = q; 
            end
        end
    end
    
    pair1 = bestpair1;
    pair2 = bestpair2;
    
    pair1;
    pair2;
    
    s = spline(beat2(pair2),beat1(pair1),t);
    q = matchQuality(s,pair1,pair2);
    
    pair1 = [1 3 4 6 7 8 9 10 12];
    pair2 = [1 3 4 5 6 7 8 9 11];          
            
    s = spline(beat2(pair2),beat1(pair1),t);
    q = matchQuality(s,pair1,pair2);
    
    figure
    hold on
    plot(t,s)
    plot(t(1:end-1),diff(s)./diff(t))
    plot(t(1:end-2),diff(s,2)./diff(t(1:end-1)).^2)

    beat3 = spline(beat2(pair2),beat1(pair1),beat2);
    figure
    hold on
    plotBeat(beat1,1)
    plotBeat(beat2.*(beat1(end)/beat2(end)),1.2)
    plotBeat(beat3,1.1)
    ylim([0 3])
    
    figure
    hold on
    plot(3:maxpairs,bestqn(3:maxpairs),'-*')
end

function q = matchQuality(s,pair1,pair2)
    %q = -norm(diff(s,2))/(numel(pair1)-2)^2;
    q = (numel(pair1)-2)/max(abs(diff(s)));
end

function plotBeat(beat, y)
    scatter(beat,y*ones(size(beat)));
end