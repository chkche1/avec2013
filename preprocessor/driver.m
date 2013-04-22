%% Process a series of audio files
wavpath = '../Training_Audio/Converted/';
wavs = dir('../Training_Audio/Converted/*.wav');
numfiles = length(wavs);
for k = 1:numfiles
    wavs(k).name
    [segs, bins] = preprocess(strcat(wavpath,wavs(k).name), 1.5);
    [p, name, ext] = fileparts(wavs(k).name);
    folderpath = strcat('../Training_Audio/',name);
    mkdir(folderpath);
    folderpath = strcat(folderpath,'/');
    csvwrite(strcat(folderpath,name,'_bins','.csv'), bins);
    segnum = length(segs);
    for i=1:segnum
       wavwrite(segs{i},strcat(folderpath,name+'.wav','_',num2str(i))); 
    end
end
