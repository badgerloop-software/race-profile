% Read the combined data file
inputFilePath = 'TestDataAnalysis\coastDownAnalysis\ReynoldsNum\combined_data.csv';
data = readtable(inputFilePath);

% Initialize arrays to store results
numRows = height(data);
densityArray = zeros(numRows, 1);
viscosityArray = zeros(numRows, 1);

% Process each row
for i = 1:numRows
    temperature = data.temperature(i);
    pressure = data.surface_pressure(i);
    humidity = data.relative_humidity(i);
    
    % Call airParams function
    [density, viscosity] = airParams(temperature, pressure, humidity);
    
    % Store results
    densityArray(i) = density;
    viscosityArray(i) = viscosity;
end

% Add results to the data table
data.density = densityArray;
data.viscosity = viscosityArray;

% Ensure output directory exists (create full path if necessary)
outputDir = 'TestDataAnalysis\coastDownAnalysis\ReynoldsNum';
if ~exist(outputDir, 'dir')
    [status, msg] = mkdir(outputDir);
    if ~status
        error('Failed to create directory: %s', msg);
    end
end

% Write results to a new CSV file
outputFilePath = fullfile(outputDir, 'combined_data_with_air_params.csv');
writetable(data, outputFilePath);
disp(['Results written to: ', outputFilePath]);

