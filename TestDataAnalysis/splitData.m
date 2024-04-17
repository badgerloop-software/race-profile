%% Splits Data
% Jacob Petrie

% Saves data from input file from times startTime to endTime to a new file
%   startTime: must be in format 'YYYY-MM-DD HH:MM:SS'
%   endTime: also must be in same format e.g '2024-04-14 16:05:24'
%   inputFilename: name (including the relative path) of the data file
%   outputFilename: name (including the relative path) of the output file
function splitData(startTime, endTime, inputFilename, outputfilename)
    DATA = readtable(inputFilename);
    
    % Convert Times to unix timestamp
    startTime   = datetime(startTime);
    endTime     = datetime(endTime);

    unixStart   = posixtime(startTime);
    unixEnd     = posixtime(endTime);

    % Create output Destination for outputs
    % folderName = outputfilename;
    % if (contains(outputfilename, '.'))
    %     folderName = extractBefore(outputfilename, '.');
    %     mkdir(folderName);
    % else 
    %     mkdir(folderName);
    % end

    inRegion = (DATA.Var1 > unixStart) & (DATA.Var1 < unixEnd);
    
    filteredData = DATA(inRegion, :);
    writetable(filteredData, outputfilename);
end