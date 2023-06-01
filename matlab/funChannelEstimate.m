% (c) 2022 Northeastern University
% Institute for the Wireless Internet of Things
% Created by Davide Villa (villa.d@northeastern.edu)

function [pathloss, cir, pdp] = funChannelEstimate(tx,rx,plots,sr)
%FUNCHANNELESTIMATE Compute estimations (pathloss, cir, pdp) of the channel.
%   INPUT: tx and rx signals, plot boolean, sample rate.
%   OUTPUT: pathloss, cir, pdp

%% Pathloss computations
% tx: tx data - rx: rx data

pathloss = 0;
cir = 0;
pdp = 0;

[corr,lags] = xcorr(rx, tx);
[~, maxCorrIdx] = max(abs(corr));   % Get max correlation index
maxCorr = corr(maxCorrIdx);         % Max correlation value

if abs(maxCorr) < 0.001             % Is this value acceptable?
    return;
end

rescale = maxCorr / (tx'*tx);       % Rescale factor (equal to /N)
pathloss = mag2db(abs(rescale));    % Pathloss value (should be same as max of pdp)


%% CIR and PDP computations

lags_time = lags*(1/sr)*1e6;        % Lags transformed in time

[corrI,lagsI] = xcorr(real(rx), tx);
corrI = corrI./length(tx);

[corrQ,lagsQ] = xcorr(imag(rx), tx);
corrQ = corrQ./length(tx);

corrIQ = corrI + 1j*corrQ;
cir = sqrt(corrI.^2 + corrQ.^2);    % Channel Impulse Response

pdpIQ = abs(cir);
pdp = mag2db(pdpIQ);                % Power Delay Profile

if plots
    figure
    plot(lags, cir)
    title('Received CIR')
    xlabel('Time (us)')
    ylabel('corr IQ')
    
    figure
    plot(lags_time, pdp)
    title('Received PDP')
    xlabel('Time (us)')
    ylabel('Path Gain [dB]')
end


end