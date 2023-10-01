%% Constants used for Car Sim

% Non-Configurable Constants
SECONDS_PER_HOUR = 3600;
SECONDS_PER_MINUTE = 60;
INCH_TO_METER = 0.0254;
UNIT_TO_KILO = 1 / 1000;
LBF_TO_KG = 0.45359237;


% Configurable Constants
TIME_RES = 10; % Seconds
PROFILE_LENGTH = 4000; % Seconds
HV_PACK_VOLTAGE = 96; % Volts; TEMPORARY until voltage curve is derived
HV_PACK_CAPACITY = 80; % 57 % Amp-hours
WHEEL_DIAMETER_METERS = 16.75 * INCH_TO_METER; % Meters
FINAL_KWH = 0; % KwH, battery level for variable time run to end
CAR_MASS = 447.90 * LBF_TO_KG; % data from CarWeightCalc.xlsx
DRIVER_MASS = 176 * LBF_TO_KG;
AIR_DENSITY = 1.2; % kg m^-3
FRONTAL_AREA = 1; %
DRAG_COEFFICIENT = 0.1; % TEMPORARY until drag curve is derived (CFD)
C_ROLLING_RESISTANCE = .0025;
GRAVITY = 9.81; % gravitational acceleration m s^-2
%MOTOR_CONSTANT = % CHECK THIS

% Controls
TARGET_SPEED = 15;
P = 1;
I = 0.01;
D = 0.01;

% Dependant Constants
WHEEL_CIRCUMFRENCE = WHEEL_DIAMETER_METERS * pi; % Meters
WHEEL_RADIUS = WHEEL_DIAMETER_METERS / 2;
FULL_PACK_KWH = HV_PACK_VOLTAGE * HV_PACK_CAPACITY * UNIT_TO_KILO; % kWh
STARTING_KWH = FULL_PACK_KWH * (1 - 0.00); % 100% State of Charge
TOTAL_MASS = CAR_MASS + DRIVER_MASS;

%% Data

% MOTOR
% Motor Eco Mode data
CURRENT_DATA_ECO = [0.780 1.37 2 3 4 5 6 8 10 12 14 16 18 20 25 30];
TORQUES_DATA_ECO = [0 0.6 1.4 2.4 3.4 4.5 5.7 7.8 10.0 12.3 14.6 16.9 19.2 21.6 27.6 34.3];
NO_TORQUE_CURRENT = CURRENT_DATA_ECO(1); % Assumes data set starts at zero
% Motor Important values
MIN_CURRENT = min(CURRENT_DATA_ECO);
MAX_CURRENT = max(CURRENT_DATA_ECO);
MAX_TORQUE = max(TORQUES_DATA_ECO);
% Motor Interpolation
INT_CURRENTS = CURRENT_DATA_ECO(1):0.0001:CURRENT_DATA_ECO(end);
INT_TORQUES_ECO = interp1(CURRENT_DATA_ECO, TORQUES_DATA_ECO, INT_CURRENTS,'spline');

% TIRE
% Rolling Resitance Coefficient (RRC) data
SPEED_DATA_TIRE = [50 80 100]; % km/h
ROLLING_RESISTANCE = [2.30 2.68 3.02]; % unitless
PRESSURE = 500 / UNIT_TO_KILO; % Pa

