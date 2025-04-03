function results = car_simulation(args)
    % Car simulation wrapper that sets up parameters and runs the simulation
    % 
    % Inputs:
    %    StopTime: Simulation stop time in seconds (default: based on profile)
    %    TargetSpeed: Speed target in m/s (default: 20)
    %    TargetPower: Power target in kW (default: 500)
    %    AirTemp: Air temperature in Celsius (default: 25)
    %    StartSoc: Starting battery state of charge (0-1, default: 1)
    %    ControlMode: Power control (1) or speed control (0) (default: 1)
    %    CourseData: Course elevation data (default: uses built-in course)
    %    WeatherData: Optional irradiance data (default: uses built-in data)
    %
    % Outputs:
    %    results: Structure with simulation results

    arguments
        args.StopTime (1,1) double = nan
        args.TargetSpeed (1,1) double = 20 
        args.TargetPower (1,1) double = 500
        args.AirTemp (1,1) double = 25
        args.StartSoc (1,1) double = 1
        args.ControlMode (1,1) {mustBeNumericOrLogical} = 1
        args.CourseData = []
        args.WeatherData = []
    end

    %% Setup default parameters (from setuptest.m)
    % Load all the setup parameters
    setuptest;
    
    %% Override parameters with input arguments
    if ~isnan(args.StopTime)
        PROFILE_LENGTH = args.StopTime;
    end
    
    TARGET_SPEED = args.TargetSpeed;
    TARGET_POWER = args.TargetPower;
    CONTROL_MODE = args.ControlMode;
    STARTING_KWH = FULL_PACK_KWH * args.StartSoc;
    
    % Override course data if provided
    if ~isempty(args.CourseData)
        if isfield(args.CourseData, 'distance') && isfield(args.CourseData, 'grade')
            DISTANCE = args.CourseData.distance;
            GRADE_ANGLE = args.CourseData.grade;
            INT_DISTANCES = DISTANCE(1):0.25:DISTANCE(end);
            INT_GRADE_ANGLE = interp1(DISTANCE, GRADE_ANGLE, INT_DISTANCES,'spline');
        end
    end
    
    % Override weather/solar data if provided
    if ~isempty(args.WeatherData)
        if isfield(args.WeatherData, 'times') && isfield(args.WeatherData, 'irradiance')
            TIMES = args.WeatherData.times;
            PROJECTED_IRRADIANCE = args.WeatherData.irradiance;
        end
    end
    
    %% Package parameters for the simulation
    params = struct();
    
    % Add all constants from workspace to params
    vars = who;
    for i = 1:length(vars)
        varName = vars{i};
        % Skip args and internal variables
        if ~strcmp(varName, 'args') && ~strcmp(varName, 'i') && ~strcmp(varName, 'vars') && ~strcmp(varName, 'params')
            params.(varName) = eval(varName);
        end
    end
    
    %% Run simulation using sim_the_model
    sim_input = struct();
    sim_input.StopTime = PROFILE_LENGTH;
    sim_input.TunableParameters = params;
    sim_input.ConfigureForDeployment = true;
    
    % Call the simulation
    results = sim_the_model(sim_input);
end