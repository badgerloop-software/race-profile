%% Data Sources
% COURSE_DATA     = 
% WEATHER_DATA    =
ECO_DATA_FILE     = 'Data/MotorDataEco.csv';
POWER_DATA_FILE   = 'Data/MotorDataEco.csv'; % Replace later

%% Constants used for Car Sim

% Non-Configurable Constants
SECONDS_PER_HOUR = 3600;
SECONDS_PER_MINUTE = 60;
INCH_TO_METER = 0.0254;
UNIT_TO_KILO = 1 / 1000;
LBF_TO_KG = 0.45359237;


% Configurable Constants
TIME_RES = 10; % Seconds
START_TIME = 9*(SECONDS_PER_HOUR) + 0*(SECONDS_PER_MINUTE); % start time of day
END_TIME = 20*(SECONDS_PER_HOUR) + 0*(SECONDS_PER_MINUTE); % end time of day
PROFILE_LENGTH = END_TIME - START_TIME; % Seconds
HV_PACK_VOLTAGE = 96; % Volts; TEMPORARY until voltage curve is derived
HV_PACK_CAPACITY = 80; % 57 % Amp-hours
WHEEL_DIAMETER_METERS = 22 * INCH_TO_METER; % Meters
FINAL_KWH = 0; % KwH, battery level for variable time run to end
CAR_MASS = 447.90 * LBF_TO_KG; % data from CarWeightCalc.xlsx
DRIVER_MASS = 176 * LBF_TO_KG;
AIR_DENSITY = 1.2; % kg m^-3
FRONTAL_AREA = 1; % 
DRAG_COEFFICIENT = 0.25; % TEMPORARY until drag curve is derived (CFD)
C_ROLLING_RESISTANCE = .0025;
GRAVITY = 9.81; % gravitational acceleration m s^-2
SPEED_TO_RPM = 60 / (WHEEL_DIAMETER_METERS * pi);
%MOTOR_CONSTANT = % CHECK THIS

% Controls
CONTROL_MODE = 1;   % power-control = 1, speed-control = 0
TARGET_SPEED = 10; % Meters / Second
ACCEL_TOLERANCE = 3;
SP = 1; %Speed P
SI = 0.01; %Speed I
SD = 0.01; %Speed D

TARGET_POWER = 5; %kW
PP = 1;
PI = 0.01;
PD = 0.01;

%Speed-Power control switch
%set_param('Car/Control/PW_SP_SW', 'sw', "1"); %power-control = 1, speed-control = 0
PW_SP = 1;
%1: power pid; 0: speed pid


%Battery Management System
MAX_SOC = 0.99;
MIN_SOC = 0.1;

%Wether Data
%TEMP = 

% Dependant Constants
WHEEL_CIRCUMFRENCE = WHEEL_DIAMETER_METERS * pi; % Meters
WHEEL_RADIUS = WHEEL_DIAMETER_METERS / 2;
FULL_PACK_KWH = HV_PACK_VOLTAGE * HV_PACK_CAPACITY * UNIT_TO_KILO; % kWh
STARTING_KWH = FULL_PACK_KWH * (1 - 0); % 100% State of Charge
TOTAL_MASS = CAR_MASS + DRIVER_MASS;

% Low Voltage
FAN_DRAW = 4.8; % Watts
DRIVER_DISPLAY_DRAW = 2.5; % Watts
HEADLIGHT_DRAW = 2; % Watts

%% Data

% Course Parameters, temporary until course data is included 
DISTANCE = [1:50e3, (1+50e3):200e3];% distance traveled along course, should be meters
fronthalf = length(1:50e3);
backhalf= length((1+50e3):200e3);
GRADE_ANGLE = -[0*ones(1,fronthalf), 0.03*ones(1,backhalf)];
%GRADE_ANGLE(1, floor(length(DISTANCE)/2):end) = 0.1*ones(1, floor(length(DISTANCE)/2) + 1);
% INPUT COURSE HERE
INT_DISTANCES = DISTANCE(1):0.25:DISTANCE(end);
INT_GRADE_ANGLE = interp1(DISTANCE, GRADE_ANGLE, INT_DISTANCES,'spline');


%% MOTOR
% Motor Eco Mode data
REGEN_ON = 0;
ECO_DATA = readmatrix(ECO_DATA_FILE);
% CURRENT_DATA_ECO = [0.780 1.37 2 3 4 5 6 8 10 12 14 16 18 20 25 30];
% TORQUES_DATA_ECO = [0 0.6 1.4 2.4 3.4 4.5 5.7 7.8 10.0 12.3 14.6 16.9 19.2 21.6 27.6 34.3];
% RPM_DATA_ECO     = 
CURRENT_DATA_ECO = ECO_DATA(:, 1);
TORQUES_DATA_ECO = ECO_DATA(:, 2);
RPM_DATA_ECO     = ECO_DATA(:, 3);
RPM_BREAKPOINTS_ECO   = flip(RPM_DATA_ECO);
MAX_CURRENTS_ECO      = flip(CURRENT_DATA_ECO);
% Motor Important values
NO_TORQUE_CURRENT_ECO = CURRENT_DATA_ECO(1); % Assumes data set starts at zero
MIN_CURRENT_ECO = min(CURRENT_DATA_ECO);
MAX_CURRENT_ECO = max(CURRENT_DATA_ECO);
MAX_TORQUE_ECO = max(TORQUES_DATA_ECO);
MAX_RPM_ECO = max(RPM_DATA_ECO);

% Motor Power Mode data
POWER_DATA = readmatrix(POWER_DATA_FILE);
CURRENT_DATA_POWER      = POWER_DATA(:, 1);
TORQUES_DATA_POWER      = POWER_DATA(:, 2) * 1; % TEMPORARY REMOVE THIS !!!!!!
RPM_DATA_POWER          = POWER_DATA(:, 3);
RPM_BREAKPOINTS_POWER   = flip(RPM_DATA_POWER);
MAX_CURRENTS_POWER      = flip(CURRENT_DATA_POWER);
% Motor Important values
NO_TORQUE_CURRENT_POWER = CURRENT_DATA_POWER(1); % Assumes data set starts at zero
MIN_CURRENT_POWER = min(CURRENT_DATA_POWER);
MAX_CURRENT_POWER = max(CURRENT_DATA_POWER);
MAX_TORQUE_POWER = max(TORQUES_DATA_POWER);
MAX_RPM_POWER = max(RPM_DATA_POWER);


%% TIRE
% Rolling Resitance Coefficient (RRC) data
SPEED_DATA_TIRE = [50 80 100]; % km/h
ROLLING_RESISTANCE = [2.30 2.68 3.02] / 1000; % unitless
PRESSURE = 500 / UNIT_TO_KILO; % Pa

%% Solar Data
% the data entered now is made up, to pull actual data from the internet
TIMES = START_TIME:1:END_TIME;
PROJECTED_IRRADIANCE = 800 * ones(size(TIMES));

% outputName = 'Outputs/results.csv';
% simulation = sim("Car.slx");
% out = simulation.logsout;
% resultsTable = out.extractTimetable;
% writetimetable(resultsTable, outputName)
