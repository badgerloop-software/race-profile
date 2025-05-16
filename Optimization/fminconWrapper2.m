%fminconWrapper2.m 

% ── Add Simulation folder to your path ────────────────────────────────────────
[thisFile,~,~] = fileparts( mfilename('fullpath') );  
simFolder     = fullfile( thisFile, '..', 'Simulation' );  
addpath( simFolder );  


%--- Set up optimization ---
initialGuess = 500;      % Initial guess for target power (kW) - adjust as needed
lowerBound = 100;       % Lower bound for target power (kW) - adjust as needed
upperBound = 1000;      % Upper bound for target power (kW) - adjust as needed

%--- Optimization Options ---
options = optimoptions('fmincon'); % Get default options structure
options.MaxFunctionEvaluations = 20; % Limit the number of function evaluations (simulations)
options.MaxIterations = 10;        % Optionally limit the number of iterations as well

%--- Run optimization using fmincon ---
optimizedPower = fmincon(@negDistance2, initialGuess, [], [], [], [], lowerBound, upperBound, [], options); % Pass options

%--- Display Results ---
fprintf('Optimized Target Power (potentially suboptimal due to limits): %.2f kW\n', optimizedPower);

%--- Get the actual maximum distance (important validation step) ---
assignin('base', 'TARGET_POWER', optimizedPower); % Set the optimized power

% --- Get PROFILE_LENGTH from base workspace for final sim ---
try
    stopTimeValue = evalin('base', 'PROFILE_LENGTH');
    if ~isnumeric(stopTimeValue) || isempty(stopTimeValue) || ~isscalar(stopTimeValue)
        error('PROFILE_LENGTH in base workspace is not a valid numeric scalar for final simulation.');
    end
catch ME
    error('Could not retrieve valid PROFILE_LENGTH from base workspace for final simulation: %s', ME.message);
end

% --- Run the simulation again with the optimized power AND explicit StopTime ---
simOut = sim('Car', 'StopTime', num2str(stopTimeValue)); % Use StopTime parameter

% --- Extract distance from the final simulation output ---
try
    logsout_data = simOut.logsout; % Access logsout from the output structure
    maxDistance = logsout_data.getElement('Position [m]').Values.Data(end); % Get the distance
    fprintf('Maximum Distance Traveled (with limited optimization): %.2f m\n', maxDistance);
catch ME
     error('Error extracting distance from final simulation output: %s. Check signal name ''Position [m]''.', ME.message);
end