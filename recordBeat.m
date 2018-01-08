function b = recordBeat()
    global a;
    a = [];
    global q;
    q = 0;
    tic;

    f = figure;
    clf(f);
    set(f, 'KeyPressFcn', @(f, eventDat)button(f, eventDat))
    drawnow;
    
    waitfor(f)
    b = a - a(1);
    
    b = b';

    function button(f, eventDat)
        if strcmp(eventDat.Key,'q')
           q = 1;
        end
        a = [a toc];
    end
end