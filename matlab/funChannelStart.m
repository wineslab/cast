% (c) 2022 Northeastern University
% Institute for the Wireless Internet of Things
% Created by Davide Villa (villa.d@northeastern.edu)

function [start_frame] = funChannelStart(tx,rx,period,startidx,endidx)
%FUNCHANNELSTART Compute estimations (pathloss, cir, pdp) of the channel.
%   INPUT: tx and rx signals, period, and initial start and end.
%   OUTPUT: start frame

%% Pathloss computations for start
% tx: tx data - rx: rx data

tmpstart = startidx;
tmpend = endidx;
trials = 100;        % trials to find out the start of the frame
for i=1:trials
    
    tmpstart = startidx+startidx*(i-1);             % Start index to look for starting point
    tmpend = endidx+endidx*(i-1);                   % End index to look for starting point
    if (tmpend > length(rx))
        tmpend = length(rx);
    end
    rx4start = rx(tmpstart:tmpend);
    
    [corr,lags] = xcorr(rx4start, tx);

    if max(abs(corr)) < 0.01                        % Find a reasonable number for this threshold
        continue;
    end

    [~, maxCorrIdx] = max(abs(corr));
    start = lags(maxCorrIdx) + 1;                   % Start of the higher correlation
    
    start = start + tmpstart;                       % Adding initial offset
    backingidx = (floor(start/period)-2);           % Number of backward computations
    
    if backingidx < 0       % Cap to 0 
        backingidx = 0;
    end
    
    start_frame = start - (backingidx * period);    % Going backward till start

    return;
end

end