%% Cleans Coast Down Data
% Jacob Petrie

function FindCoastDown(inputfilename, outputfilename)
    DATA = readtable(inputfilename);

    % Create output Destination for outputs
    folderName = outputfilename;
    if (contains(outputfilename, '.'))
        folderName = extractBefore(outputfilename, '.');
        mkdir(folderName);
    else 
        mkdir(folderName);
    end

    % Identify Coast Down regions
    regionNum = 1;

    while true
        % 

        % Populate destination
        regionNum = regionNum + 1;
    end
    

end