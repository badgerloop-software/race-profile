% Specify the folder path
folder_path = pwd;
folder_path = join([folder_path, '/coasts2024-04-141530/']);

% Get a list of files in the folder
files = dir(fullfile(folder_path, '*.csv'));

% Iterate over each file
for i = 1:numel(files)
    % Get the file name
    file_name = join([folder_path, files(i).name]);
    
    % Perform operations with the file, for example:
    % Read the file
    file_data = readtable(file_name);
    
    startTime = file_data.Var1(1);
    plot(file_data.Var1 - startTime, file_data.speed)
    hold on
end
