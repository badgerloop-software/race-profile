%% Telemetry Analysis
% Jacob Petrie

%% Convert to Function
filename = "Data/TelemetryMS.xlsx";

DATA = readtable(filename);

mass = 283; % KG
rho = 1.2; % density of air, kg/m^3, can change with altitude
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
dragCoeff = dragForce ./ ( 0.5 * rho * A * (speeds(1:(end-1)).^2) );

% Calculate Drag coefficient at each speed

%% Functions

% Model for rolling resistance as a funciton of velocity
% Source: Ben Colby
function rr = rollingResistance(speed, normalForce)
    C_rr = 0.0017 .* exp(0.0054 .* speed);
    rr = C_rr * normalForce;
end