function [ seg, bins] = preprocess(wavFileName, threshold)
%PREPROCESS Summary of this function goes here
%   Detailed explanation goes here
%
% ARGUMENTS:
% - wavFileName - wave file
% - threshold - the cut value length for all segments
%
% RETURNS:
% - seg: a cell array with audio segments all longer than threshold
% - bins: pause length distribution
% 
% EXECUTION EXAMPLE:
%
% seg = preprocess('example.wav', 2)
%
narginchk(2,2);
[segments, fs, Limits] = detectVoiced(wavFileName);
numRows = size(segments, 2);

for i=1:numRows
    leng = size(segments{i},1)
    if leng/fs < threshold
        segments{i} = [];
    end
end
bins = zeros(1, 100);
for i=1:numRows
    if(isempty(segments{i}))
        continue;
    end
    if(i<numRows)
        % dif is in msec
        dif = (Limits(i+1,2) - Limits(i,1)) / fs * 1000;
        bucket_no = dif/int32(100);
        if(bucket_no==0)
            continue;
        end
        if(bucket_no>100)
            bucket_no = 100;
        end
        bins(bucket_no) = bins(bucket_no)+1;
    end
end

seg = segments(~cellfun(@isempty,segments)); 
end

