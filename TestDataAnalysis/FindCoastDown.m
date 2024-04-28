%% Cleans Coast Down Data
% Jacob Petrie

function FindCoastDown(inputfilename, outputfilename)
    % all data from file
    DATA = readtable(inputfilename);

    filetype = ''; % Used later to write data

    % Create output Destination for outputs
    folderName = outputfilename;
    if (contains(outputfilename, '.'))
        folderName = extractBefore(outputfilename, '.');
        mkdir(folderName);
        filetype = join(['.', extractAfter(outputfilename, '.')]);
    else
        mkdir(folderName);
        filetype = '.csv';
    end
    
    % Identify Coast Down regions
    isCoasting = (DATA.speed > 10) ...              % Car is moving
               & (DATA.accelerator_pedal == 0)...   % Car is not motoring
               & (DATA.foot_brake == 0);            % Car is not braking
    
    % filter to coast downs that are of a certain length
    numSeconds = 5;
    unitConversion = 1000; % Timestamps are given in milliseconds
    
    % Find runs of adjacent true values in isCoasting
    differences = diff([false; isCoasting; false]);
    startIndices = find(differences == 1);
    endIndices = find(differences == -1);
    
    % Filter isCoasting for runs lasting longer than numSeconds
    isCoastingFiltered = false(size(isCoasting));
    numCoasts = 0;
    for i = 1:numel(startIndices)
        endTime = DATA{endIndices(i),1};
        startTime = DATA{startIndices(i),1};
        thisCoastIndices = startIndices(i):endIndices(i);
        
        if (endTime - startTime)/unitConversion > numSeconds
            numCoasts = numCoasts + 1;
            isCoastingFiltered(thisCoastIndices) = true;

            % Save coast to a file
            filepath = join([folderName, '/']);
            name = join([folderName, '(', num2str(numCoasts), ')', filetype]);
            fullName = join([filepath, name]);
            writetable(DATA(thisCoastIndices, :), fullName);
        end
               
    end

    % coastData = DATA(isCoasting, :);
    % 
    % while true
    %     % 
    % 
    %     % Populate destination
    %     regionNum = regionNum + 1;
    % end
    % 
    % figure
    % plot(coastData.Var1, coastData.speed, '-*');
    % figure
    % plot(isCoastingFiltered)
    
    
end