% The following data was pulled from a Mitsuba Data Sheet:
currents_eco = [0.780 1.37 2 3 4 5 6 8 10 12 14 16 18 20 25 30]';
torques_eco = [0 0.6 1.4 2.4 3.4 4.5 5.7 7.8 10.0 12.3 14.6 16.9 19.2 21.6 27.6 34.3]';

% How many data points to include in interpolated model
numPoints = 500; 

interpedCurrents = linspace(min(currents), max(currents), numPoints)';
interpedTorques = interp1(currents, torques, interpedCurrents, 'spline');

% Uncomment to see relationship:
% plot(interpedCurrents, interpedTorques)

% Format interpolated Data and save to file:
T = table(interpedCurrents,interpedTorques,'VariableNames',["Current","Torque"]);
writetable(T, 'MotorDataEco.csv')



