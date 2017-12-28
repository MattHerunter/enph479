function beat3 = matchBeatsLinear(beat1,beat2)
    beat2_unscaled = beat2;
    beat2 = beat2.*(beat1(end)-beat1(1))/(beat2(end)-beat2(1));
    t = linspace(0,beat1(end),1000);
    
    bestq = -inf;
    bestpair1 = [];
    bestpair2 = [];
    
    maxpairs = min(numel(beat1)-2,numel(beat2)-2);
    minpairs = 3;
    bestqn = -inf*(1:maxpairs);
    
    algorithm = 2;
    
    if algorithm == 0
        % Brute force search over pairings. Use to test quality functions
        % and as a benchmark for heuristic approaches.
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

                q = matchQuality(beat1,beat2,pair1,pair2);
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
    elseif algorithm == 1
        % BAD ALGORITHM
        % Local search that starts with a bad pairing and searches for
        % 'neighbor' pairings with better quality. This doesn't really
        % work right now, gets stuck easily in local maxima.
        for numpairs = minpairs:maxpairs
            pair1 = [1 2:(numpairs+1) numel(beat1)];
            pair2 = [1 2:(numpairs+1) numel(beat2)];

            while 1
                changed = 0;
                for ii = (numel(pair1)-1):-1:2
                    bestqual = -inf
                    bestp1 = [];
                    bestp2 = [];
                    for p1 = (pair1(ii-1)+1):(pair1(ii+1)-1)
                        for p2 = (pair2(ii-1)+1):(pair2(ii+1)-1)
                            tempL = (beat2(p2)-beat2(pair2(ii-1)))/(beat1(p1)-beat1(pair1(ii-1)));
                            tempR = (beat2(pair2(ii+1))-beat2(p2))/(beat1(pair1(ii+1))-beat1(p1));
                            durL = beat1(p1)-beat1(pair1(ii-1));
                            durR = beat1(pair1(ii+1))-beat1(p1);

                            qual = -((tempL-1).^2 * durL + (tempR-1).^2 * durR);
                            qual
                            if qual > bestqual
                                bestqual = qual;
                                bestp1 = p1;
                                bestp2 = p2;
                            end
                        end
                    end

                    if (bestp1 == pair1(ii)) && (bestp2 == pair2(ii))
                        %changed = 0;
                    else
                        changed = 1;
                        pair1(ii) = bestp1;
                        pair2(ii) = bestp2;
                    end
                end

                if changed == 0
                    break;
                end
            end

            %pair1
            %pair2

            q = matchQuality(beat1,beat2,pair1,pair2);
            bestqn(numpairs) = q;

            if q > bestq
            %if numpairs == 5
                bestq = q;
                bestpair1 = pair1;
                bestpair2 = pair2;
            end
        end
    elseif algorithm == 2
        % Heuristic algorithm that goes from the beginning to the end of
        % the track and creates a pairing for each note if the pairing
        % exceeds a quality threshold.
        
        for numpairs = minpairs:maxpairs % Numpairs is a garbage variable here, just used for the graphing...
            threshold = -0.5/numpairs; %How to define a reasonable quality threshold?
            
            tempbeat1 = beat1;
            tempbeat2 = beat2;
            
            %First notes in each track always paired, currently.
            pair1 = [1];
            pair2 = [1];
            
            previi = 1;
            % Iterate over beats in 'beat1'.
            for ii = 2:(numel(beat1)-1)
                qual = -inf;
                bestjj = 0;
                prevjj = pair2(end);
                % Iterate over potential pairing candidates from 'beat2'
                for jj = (pair2(end)+1):(numel(beat2)-1)
                    
                    temp = (tempbeat2(jj)-tempbeat2(pair2(end)))/(tempbeat1(ii)-tempbeat1(pair1(end)));
                    dur = (tempbeat1(ii)-tempbeat1(pair1(end)));
                    tempqual = -(temp-1)^2 * dur;
                    
                    % Keep track of best pairing candidate.
                    if tempqual > qual
                       qual = tempqual;
                       bestjj = jj;
                    end
                end
            
                % Only add the pairing if quality exceeds threshold.
                % Otherwise, the beat from 'beat1' is left unpaired.
                if qual > threshold
                    jj = bestjj;
                    pair1 = [pair1 ii];
                    pair2 = [pair2 jj];
                    
                    % Adjust 'beat2' timings to synchronize the paired
                    % notes.
                    stretchL = (tempbeat1(ii)-tempbeat1(previi))/(tempbeat2(jj)-tempbeat2(prevjj));
                    stretchR = (tempbeat1(end)-tempbeat1(ii))/(tempbeat2(end)-tempbeat2(jj));
                    
                    tempbeat2(prevjj:jj-1) = tempbeat2(prevjj)+(tempbeat2(prevjj:jj-1)-tempbeat2(prevjj))*stretchL;
                    tempbeat2(jj:end) = tempbeat2(end)-(tempbeat2(end)-tempbeat2(jj:end))*stretchR;
                    
                    previi = ii;
                    prevjj = jj;
                end
            end
            
            % Last notes in each track always paired, currently.
            pair1 = [pair1 numel(beat1)];
            pair2 = [pair2 numel(beat2)];
            
            q = matchQuality(beat1,beat2,pair1,pair2);
            bestqn(numpairs) = q;
            
            % If we tried multiple quality thresholds, keep track of the best
            % pairing
            if q > bestq
                bestq = q;
                bestpair1 = pair1;
                bestpair2 = pair2;
            end
        end
    end
    
    pair1 = bestpair1;
    pair2 = bestpair2;
    
    pair1
    pair2
    matchQuality(beat1,beat2,pair1,pair2)
    
    %figure
    %hold on
    %plot(t,s)
    %plot(t(1:end-1),diff(s)./diff(t))
    %plot(t(1:end-2),diff(s,2)./diff(t(1:end-1)).^2)

    beat3 = spline(beat2(pair2),beat1(pair1),beat2);
    figure
    hold on
    EC1 = [0 0 1];
    FC1 = [0.4 0.6 0.8];
    EC2 = [1 0 0];
    FC2 = [0.8 0.6 0.4];
    plotBeat(beat1,0.3,EC1,FC1)
    %plotBeat(beat2.*(beat1(end)/beat2(end)),2.0)
    plotBeat(beat2_unscaled,2.2,EC2,FC2)
    plotBeat(beat1,1.9,EC1,FC1)
    x = [beat1(pair1);beat2_unscaled(pair2)];
    y = [1.9;2.2];
    plot(x,y,'--k')
    plotBeat(beat3,0.6,EC2,FC2)
    x = [beat1(pair1);beat3(pair2)];
    y = [0.3;0.6];
    plot(x,y,'k')
    ylim([0 3])
    %xlim([-0.2 3.1])
    
    set(gca,'xtick',[])
    set(gca,'ytick',[])
    set(gca,'visible','off')
    
    figure
    hold on
    plot(3:maxpairs,bestqn(3:maxpairs),'-*')
end

function q = matchQuality(beat1,beat2,pair1,pair2)
    tempo = [];
    duration = [];
    for qq = 1:numel(pair2)-1
        temp = (beat2(pair2(qq+1))-beat2(pair2(qq)))/(beat1(pair1(qq+1))-beat1(pair1(qq)));
        tempo = [tempo temp];
        dur = beat1(pair1(qq+1))-beat1(pair1(qq));
        duration = [duration dur];
    end
    
    q = (numel(pair1)-2)/(dot((tempo-1).^2,duration)+1);
end

function plotBeat(beat, y, edgecolor, facecolor)
    scatter(beat,y*ones(size(beat)),50,'o','MarkerEdgeColor',edgecolor,'MarkerFaceColor',facecolor);
end