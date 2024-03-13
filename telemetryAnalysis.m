%% Telemetry Analysis
% Jacob Petrie

%% Convert to Function
filename = "Data/TelemetryMS.xlsx";

DATA = readtable(filename);

mass = 283; % KG

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


% Calculate Drag coefficient at each speed
