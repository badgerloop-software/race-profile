% Example script for using telemetry data in simulation

% Load the telemetry data
data = load('telemetry_sim_data.mat');

% Display data summary
fprintf('Telemetry Data Summary:\n');
fprintf('Duration: %.1f seconds\n', data.sim_time(end));
fprintf('Sample count: %d\n', length(data.sim_time));

% Create time series objects for Simulink
speed_ts = timeseries(data.speed, data.sim_time, 'Name', 'Vehicle Speed');
power_ts = timeseries(data.motor_power, data.sim_time, 'Name', 'Motor Power');
voltage_ts = timeseries(data.battery_voltage, data.sim_time, 'Name', 'Battery Voltage');
current_ts = timeseries(data.battery_current, data.sim_time, 'Name', 'Battery Current');
solar_ts = timeseries(data.solar_power, data.sim_time, 'Name', 'Solar Power');
temp_ts = timeseries(data.ambient_temperature, data.sim_time, 'Name', 'Ambient Temperature');

% Plot comparison between telemetry and simulation
figure('Name', 'Telemetry vs Simulation Comparison');

% Speed comparison
subplot(3,1,1);
plot(data.sim_time, data.speed, 'b', 'DisplayName', 'Telemetry');
hold on;
% Add simulated speed here after running simulation
% plot(sim_out.speed.time, sim_out.speed.data, 'r', 'DisplayName', 'Simulation');
title('Vehicle Speed Comparison');
xlabel('Time (s)');
ylabel('Speed (mph)');
legend;
grid on;

% Power comparison
subplot(3,1,2);
plot(data.sim_time, data.motor_power, 'b', 'DisplayName', 'Telemetry');
hold on;
% Add simulated power here after running simulation
% plot(sim_out.power.time, sim_out.power.data, 'r', 'DisplayName', 'Simulation');
title('Motor Power Comparison');
xlabel('Time (s)');
ylabel('Power (W)');
legend;
grid on;

% Battery comparison
subplot(3,1,3);
plot(data.sim_time, data.battery_voltage .* data.battery_current, 'b', 'DisplayName', 'Telemetry');
hold on;
% Add simulated battery power here after running simulation
% plot(sim_out.battery_power.time, sim_out.battery_power.data, 'r', 'DisplayName', 'Simulation');
title('Battery Power Comparison');
xlabel('Time (s)');
ylabel('Power (W)');
legend;
grid on;

% Calculate error metrics
% Uncomment after running simulation
% speed_rmse = sqrt(mean((data.speed - sim_out.speed.data).^2));
% power_rmse = sqrt(mean((data.motor_power - sim_out.power.data).^2));
% fprintf('\nError Metrics:\n');
% fprintf('Speed RMSE: %.2f mph\n', speed_rmse);
% fprintf('Power RMSE: %.2f W\n', power_rmse);
