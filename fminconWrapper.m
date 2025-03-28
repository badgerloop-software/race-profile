%fminconWrapper.m 

%--- Set up optimization ---
initialGuess = 500;      % Initial guess for target power (kW) - adjust as needed
lowerBound = 100;       % Lower bound for target power (kW) - adjust as needed
upperBound = 1000;      % Upper bound for target power (kW) - adjust as needed

%--- Optimization Options ---
options = optimoptions('fmincon'); % Get default options structure
options.MaxFunctionEvaluations = 20; % Limit the number of function evaluations (simulations)
options.MaxIterations = 10;        % Optionally limit the number of iterations as well

%--- Run optimization using fmincon ---
optimizedPower = fmincon(@negDistance, initialGuess, [], [], [], [], lowerBound, upperBound, [], options); % Pass options

%--- Display Results ---
fprintf('Optimized Target Power (potentially suboptimal due to limits): %.2f kW\n', optimizedPower);

%--- Get the actual maximum distance (important validation step) ---
assignin('base', 'TARGET_POWER', optimizedPower); % Set the optimized power
sim('Car'); % Run the simulation again with the optimized power
out = sim('Car').logsout;
maxDistance = out.getElement('Position [m]').Values.Data(end); % Get the distance
fprintf('Maximum Distance Traveled (with limited optimization): %.2f m\n', maxDistance);


