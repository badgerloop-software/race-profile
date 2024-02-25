%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% This initializes all variables and data for running the "Car.slx"
% simulink model of a solar car using spreadsheet data
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%% Unit Conversions:
    SECONDS_PER_HOUR = 3600;
    SECONDS_PER_MINUTE = 60;
    INCH_TO_METER = 0.0254; 
    UNIT_TO_KILO = 1 / 1000;
    LBF_TO_KG = 0.45359237;

%% Simulation Parameters
% Time
    MAX_TIME_STEP   = 300;  % seconds, time step will never be longer than this
    START_TIME      = 0;    % seconds,
    END_TIME        = 0;    % seconds
    PROFILE_LENGTH  = END_TIME - START_TIME; % seconds, duration of sim


%% Car Properties:
% Mass Properties
    CAR_MASS = 447.90 * LBF_TO_KG;  % data from CarWeightCalc.xlsx
    DRIVER_MASS = 176 * LBF_TO_KG;  % driver plus ballast
    TOTAL_MASS = CAR_MASS + DRIVER_MASS; % total mass of the vehicle

% Dimensions
    WHEEL_DIAMETER_METERS = 22 * INCH_TO_METER;
    FRONTAL_AREA = 1.262;   % meters^2, Source: Ben Colby

% Misc Electronics
    Fan_draw = 4.8;             % Watts
    Driver_display_draw = 2.5;  % Watts
    Headlight_draw = 2;         % Watts


%% Load in data from sheets (constant values also included for testing):
% Elevation data:
    Elevation_filename = 'Data/flat_course.csv';
    %Elevation_filename = "ASC2022.csv"
    %Elevation_filename = "ASC2024.csv"
    
    Course = readtable(Elevation_filename);
    distance = Course.distance;
    elevation = Course.elevation;
    slope = Course.slope;
    
% Solar data
    solar_filename = 'Data/const_solar.csv';
    % solar_filename = '';
    Solar = readtable(solar_filename);
    times = Solar.Time;
    irradiance = Solar.Irradiance;
    
    
% Aerodynamic Data
    drag_filename = 'Data/const_drag.csv';
    % drag_filename = '';
    Drag = readtable(drag_filename);
    speeds = Drag.velocity;
    
    
% Battery Data
    battery_filename = 'Data/const_battery.csv';
    % battery_filename = '';
    Battery = readtable(battery_filename);
    SOC = Battery.SOC;
    voltage = Battery.Voltage;
    
    
% Tire Data
    % we may treat this with a best fit line instead
    C_RR = 0.0017 .* exp(0.0054 .* speeds); % SOURCE: Ben Colby
    
    
% Motor Data
    motorEco_filename   = 'Data/MotorDataEco.csv';
    %motorPower_filename = '';
    Motor               = readtable(motorEco_filename);
    currents_eco        = Motor.Current;
    Torque_eco          = Motor.Torque;
    RPM_eco             = Motor.RPM;

% Target Speed
    CruiseSpeed_filename    = 'Data/constTargetSpeed.csv';
    Cruise                  = readtable(CruiseSpeed_filename);
    distance                = Cruise.distance;
    speeds                  = Cruise.TargetSpeed;
    
% Air Density
    density_filename        = 'Data/constDensity.csv';

    
    
%% Run Simulation:
sim("Car.slx")


%% Save Data:





