% The following data was pulled from a Mitsuba Data Sheet:
currents_eco    = [0.780 1.37 2 3 4 5 6 8 10 12 14 16 18 20 25 30]';
torques_eco     = [0 0.6 1.4 2.4 3.4 4.5 5.7 7.8 10.0 12.3 14.6 16.9 19.2 21.6 27.6 34.3]';
RPMs_eco        = [893 888 884 881 877 873 869 859 852 843 834 825 818 808 788 756]';

% How many data points to include in interpolated model
numPoints = 1000; 

interpedCurrents = linspace(min(currents_eco), max(currents_eco), numPoints)';
interpedTorques = interp1(currents_eco, torques_eco, interpedCurrents, 'spline');
interpedRPMs = interp1(currents_eco, RPMs_eco, interpedCurrents, 'spline');

% Uncomment to see relationship:
hold on
plot(interpedCurrents, interpedTorques)
plot(interpedCurrents, interpedRPMs)
hold off

% Format interpolated Data and save to file:
T = table(interpedCurrents,interpedTorques, interpedRPMs,'VariableNames',["Current","Torque", "RPM"]);
writetable(T, 'MotorDataEco.csv')