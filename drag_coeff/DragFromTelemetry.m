%% Telemetry Analysis
% Jacob Petrie

function DragFromTelemetry(telemetryFilename, outputFilename, airDensity, mass)
    DATA = readtable(telemetryFilename);

    A = 1.262; % frontal area, m^2, Source: Ben Colby
    gravity = 9.81; % m/s
    weight = mass * gravity;
    
    %% Compute acceleration at every instant
    times = DATA.Var1; % no column header for the timestamps so it is 'var1' by default
    speeds = DATA.speed;
    
    % Unit conversion
    mphToMetersPerSecond = 0.44704;
    millisecondsToSecond = 1/1000;
    
    times = times .* millisecondsToSecond;
    speeds = speeds .* mphToMetersPerSecond;
    
    % Calculate acceleration
    accel = diff(speeds) ./ diff(times); % TODO: convert from forward to central difference
    force = mass * accel;
    
    % Subtract off rolling resistance
    dragForce = force - rollingResistance(speeds(1:(end-1)), weight);
    dragCoeff = dragForce ./ ( 0.5 * airDensity * A * (speeds(1:(end-1)).^2) );
    
    % Calculate Drag coefficient at each speed
end