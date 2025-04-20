%% Script to generate the python package
ME = [];
origDir = pwd;

try
    %% Add current dir to the path and cd to temporary dir
    addpath(origDir);
    scriptPath = fileparts(mfilename('fullpath'));
    addpath(scriptPath);  % Add the current directory to the path
    
    tempDir = tempname;
    mkdir(tempDir);
    cd(tempDir);
    fprintf('\n==> Created and cd''ed to %s\n', pwd);

    %% Generate the python package around car_simulation function
    % Make sure car_simulation.m is in the MATLAB path
    carSimPath = which('car_simulation');
    if isempty(carSimPath)
        error('car_simulation.m not found in the MATLAB path');
    end
    fprintf('Using car_simulation from: %s\n', carSimPath);
    
    % Use consistent directory name (car_sim_package)
    outDir = fullfile(origDir,'data_pipeline','car_package');
    if exist(outDir,'dir')
        rmdir(outDir,'s');
    end
    
    % Generate package with car_simulation as entry point
    fprintf('Starting Python package build to %s...\n', outDir);
    try
        compiler.build.pythonPackage(carSimPath, ...
            'PackageName','car1_sim', ...
            'OutputDir',outDir, ...
            'Verbose', true);  % Add verbose flag
        fprintf('Python package build completed successfully\n');
    catch buildErr
        fprintf('ERROR during package build:\n%s\n', buildErr.message);
        rethrow(buildErr);
    end

    %% Display the command to run to install the generated python package
    fprintf('\n==> Run the commands below to install the Python package:\n');
    fprintf('cd "%s"\n', outDir);
    pkgDir = fullfile(origDir,'data_pipeline','car_package');
    fprintf('python setup.py install --prefix="%s"\n\n', pkgDir);

catch ME
    disp('Error occurred during package generation:');
    disp(ME.getReport());
end

%% Cleanup
rmpath(origDir);
rmpath(scriptPath);
cd(origDir);
if exist('tempDir', 'var') && exist(tempDir, 'dir')
    rmdir(tempDir,'s');
end

%% Display completion message or rethrow errors
if isempty(ME)
    fprintf('==> Package generation complete. Follow the instructions above.\n');
else 
    ME.throw();
end