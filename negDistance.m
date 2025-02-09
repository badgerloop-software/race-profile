% negDistance.m (Your Wrapper Function)
function negDistance = negDistance(targetPower) 
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
    assignin('base', 'TARGET_POWER', targetPower);  % Assumes your Simulink model reads TARGET_POWER

    % --- Run the Simulink Simulation ---
    sim('Car');  % Make sure 'Car' is the correct name of your Simulink model

    % --- Extract the distance traveled (final position)---
    out = sim('Car').logsout; 
    distance = out.getElement('Position [m]').Values.Data(end);  % Corrected signal name!

    % --- Return the negative distance (for maximization) ---
    negDistance = -distance;
end