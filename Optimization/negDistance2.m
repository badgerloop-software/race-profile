% negDistance2.m (Your Wrapper Function)
function negDistance = negDistance2(targetPower) 
% negDistance - Wrapper function for fmincon to optimize target power
    %
    %   negDistance = negDistance(targetPower)
    %
    %   Inputs:
    %       targetPower - The target power to simulate (kW)
    %
    %   Outputs:
    %       negDistance - The negative of the final position (distance traveled)
    %

    % --- Update TARGET_POWER in the workspace ---
    assignin('base', 'TARGET_POWER', targetPower);  

    % --- Get PROFILE_LENGTH from base workspace ---
    try
        stopTimeValue = evalin('base', 'PROFILE_LENGTH');
        if ~isnumeric(stopTimeValue) || isempty(stopTimeValue) || ~isscalar(stopTimeValue)
            error('PROFILE_LENGTH in base workspace is not a valid numeric scalar.');
        end
    catch ME
        error('Could not retrieve valid PROFILE_LENGTH from base workspace: %s', ME.message);
    end

    % --- Run simulation with explicit StopTime ---
    % Use 'StopTime' parameter pair, converting the value to a string
    simOut = sim('Car', 'StopTime', num2str(stopTimeValue)); 
    
    % --- Extract distance ---
    try
        % Access logsout directly from the simOut structure
        logsout_data = simOut.logsout; 
        % Get the position signal data
        positionSignal = logsout_data.getElement('Position [m]'); % Use the correct signal name
        distance = positionSignal.Values.Data(end); 
    catch ME
        error('Error extracting distance from simulation output: %s. Check signal name ''Position [m]''.', ME.message);
    end
    
    negDistance = -distance;

end