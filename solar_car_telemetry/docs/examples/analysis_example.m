% Example MATLAB script for analyzing telemetry data

% Load the telemetry data
data = load('race_data.mat');

% Convert timestamps to datetime
timestamps = datetime(data.time/1000, 'ConvertFrom', 'posixtime');

% Create a new figure with subplots
figure('Name', 'Solar Car Telemetry Analysis', 'Position', [100 100 1200 800]);

% Plot 1: Vehicle Speed
subplot(2,2,1);
plot(timestamps, data.vehicle_speed, 'LineWidth', 1.5);
title('Vehicle Speed Over Time');
xlabel('Time');
ylabel('Speed (mph)');
grid on;

% Plot 2: Battery Power
subplot(2,2,2);
power = data.pack_voltage .* data.pack_current;
plot(timestamps, power, 'LineWidth', 1.5);
title('Battery Power');
xlabel('Time');
ylabel('Power (W)');
grid on;

% Plot 3: Temperatures
subplot(2,2,3);
plot(timestamps, data.battery_temp, 'r', ...
     timestamps, data.motor_temp, 'b', ...
     'LineWidth', 1.5);
title('System Temperatures');
xlabel('Time');
ylabel('Temperature (°C)');
legend('Battery', 'Motor');
grid on;

% Plot 4: Energy Consumption
subplot(2,2,4);
energy = cumtrapz(data.time/1000/3600, power);  % Convert to Wh
plot(timestamps, energy, 'LineWidth', 1.5);
title('Cumulative Energy Consumption');
xlabel('Time');
ylabel('Energy (Wh)');
grid on;

% Calculate some statistics
fprintf('\nRace Statistics:\n');
fprintf('Average Speed: %.1f mph\n', mean(data.vehicle_speed));
fprintf('Max Speed: %.1f mph\n', max(data.vehicle_speed));
fprintf('Total Energy Used: %.1f Wh\n', energy(end));
fprintf('Average Power: %.1f W\n', mean(power));
fprintf('Max Battery Temp: %.1f °C\n', max(data.battery_temp));
fprintf('Max Motor Temp: %.1f °C\n', max(data.motor_temp));

% Save the figure
savefig('telemetry_analysis.fig');
print('telemetry_analysis.png', '-dpng', '-r300');
