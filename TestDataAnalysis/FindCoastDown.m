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
    isCoasting = (DATA.speed > 10) & (DATA.acceletator_pedal == 0);
    % !!!!!!!!!!!ADD CONDITION TO ENSURE NOT BREAKING!!!!!!!!!!!!!
    
    % filter to coast downs that are of a certain length
    numSeconds = 5;
    unitConversion = 1000; % Timestamps are given in milliseconds

    % Find runs of adjacent true values in isCoasting
    differences = diff([false; isCoasting; false]);
    startIndices = find(differences == 1);
    endIndices = find(differences == -1);
    
    % Filter isCoasting for runs lasting longer than numSeconds
    isCoastingFiltered = false(size(isCoasting));
    for i = 1:numel(startIndices)
        endTime = DATA{endIndices(i),1};
        startTime = DATA{startIndices(i),1};
        if (endTime - startTime)/unitConversion > numSeconds
            isCoastingFiltered(startIndices(i):endIndices(i)) = true;
        end
    end

    coastData = DATA(isCoasting, :);
    
    % while true
    %     % 
    % 
    %     % Populate destination
    %     regionNum = regionNum + 1;
    % end

    % plot(coastData.Var1, coastData.speed, '-*');
    plot(isCoastingFiltered)
    

end