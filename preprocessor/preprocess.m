function [ seg, num_pauses] = preprocess(wavFileName, threshold)
%PREPROCESS Summary of this function goes here
%   Detailed explanation goes here
%
% ARGUMENTS:
% - segs: a cell array of audio segments
% - rate: sampling freq. of the audio signal
% - threshold: the threshold value (in seconds)
%
% RETURNS:
% - seg: a cell array with audio segments all longer than threshold
%
% 
% EXECUTION EXAMPLE:
%
% seg = removeShortUtterance(segs, 44100, 2)
%
[segments, fs, Limits] = detectVoiced(wavFileName);
numRows = size(segments, 2); num_pauses = 0;
pause_threshold = 0.25*fs;
pause_upper_bound = 5*fs;
for i=1:numRows
    leng = size(segments{i},1)
    if leng/fs < threshold
        segments{i} = [];
    end
end

for i=1:numRows
    if(isempty(segments{i}))
        continue
    end
    if(i<numRows)
        dif = Limits(i+1,2) - Limits(i,1)
        if(dif>=pause_threshold && dif<=pause_upper_bound)
            num_pauses = num_pauses+1
        end
    end
end

seg = segments(~cellfun(@isempty,segments)); 
end

