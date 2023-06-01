% (c) 2022 Northeastern University
% Institute for the Wireless Internet of Things
% Created by Davide Villa (villa.d@northeastern.edu)

function [iq, t] = funLoadGnuradioTrace(filename, read_size, read_offset)
% funLoadGnuradioTrace Load gnuradio trace.
%   INPUT: filename, size of the file to read (0 all).
%   OUTPUT: iq, time


fid = fopen(filename, 'rb');                    % Open file stream
if read_offset > 0                              % Set offset in start reading
    fseek(fid, read_offset, 'bof');
end
if read_size == 0                               % Read all of it
    values = fread(fid, Inf, 'float32');
else                                            % Read just part of it
    values = fread(fid, read_size, 'float32');
end

I = values(1:2:end);
Q = values(2:2:end);

iq = I + 1j*Q;
t = (0:length(iq)-1) / 1e6;     % This should take into account the used sample rate

% Force row vectors
iq = iq(:).';
t = t(:).';

end