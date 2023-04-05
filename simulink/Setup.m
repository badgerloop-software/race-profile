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
HV_PACK_VOLTAGE = 96; % Volts
HV_PACK_CAPACITY = 80; %57 % Amp-hours
WHEEL_DIAMETER_METERS = 16.75 * INCH_TO_METER; % Meters
FINAL_KWH = 0; % KwH, battery level for variable time run to end
CAR_MASS = 447.90 * LBF_TO_KG; % data from CarWeightCalc.xlsx
DRIVER_MASS = 176 * LBF_TO_KG;
AIR_DENSITY = 1.2; % kg m^-3
FRONTAL_AREA = 1; %

% Controls
TARGET_SPEED = 25;
P = 1;
I = 0.01;
D = 0.01;

% Dependant Constants
WHEEL_CIRCUMFRENCE = WHEEL_DIAMETER_METERS * pi; % Meters
FULL_PACK_KWH = HV_PACK_VOLTAGE * HV_PACK_CAPACITY * UNIT_TO_KILO; % kWh
STARTING_KWH = FULL_PACK_KWH * (1 - 0.00); % 100% State of Charge
TOTAL_MASS = CAR_MASS + DRIVER_MASS;
