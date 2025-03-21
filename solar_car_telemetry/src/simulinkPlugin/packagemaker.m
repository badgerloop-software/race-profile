%% Script to generate the python package to run sim_the_model MATLAB function
%
% By Murali Yeddanapudi on 06-Mar-2022

ME = [];
origDir = pwd;

try

    %% Add current dir to the path and cd to temporary dir
    addpath(origDir);
    tempDir = tempname;
    mkdir(tempDir);
    cd(tempDir);
    fprintf('\n==> Created and cd''ed to %s\n', pwd);

    %% Optional. call sim_the_model in MATLAB to make sure that it works correctly.
    % setup2

    %% Generate the python package around a deployed version of the_model.
    appFile = which('setuptest');
    outDir = fullfile(origDir,'solar_car_telemetry\src','car2_package');
    if exist(outDir,'dir')
        rmdir(outDir,'s');
    end
    compiler.build.pythonPackage(appFile, ...
        'PackageName','sim_the_model', ...
        'OutputDir',outDir);

    %% Display the command to run to install the generated python package
    fprintf('==> Run the commands below to install the python package\n');
    fprintf('    The location chosen here is same as the python script.\n\n');
    fprintf('cd %s\n', outDir);
    pkgDir = fullfile(origDir,'solar_car_telemetry\src','car2_package');
    fprintf('python setup.py install --prefix=\"%s\"\n\n',pkgDir);
    % input('==> One you are done runing the above commands, press any key to continue','s');

catch ME
    disp(ME.getReport());
end

%% Cleanup
rmpath(origDir);
cd(origDir);
rmdir(tempDir,'s');

%% Rethrow errors, if any
if ~isempty(ME), ME.throw(); end