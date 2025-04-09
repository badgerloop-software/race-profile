function rr = rollingResistance(speed, normalForce)
%ROLLINGRESISTANCE Summary of this function goes here
%   calculates rolling resistance based on:
%
%   speed       - The speed of the car
%   normalForce - The force of the car perpendicular to the ground
%                 (Equal to the weight on flat ground)
%
%   Calculation based on a fit performed by Ben Colby, on data from
%   bridgestone data sheet. Data sheet contains limited data:
%
%       SPEED_DATA_TIRE    = [50 80 100]; % km/h
%       ROLLING_RESISTANCE = [2.30 2.68 3.02] / 1000; % unitless
%       PRESSURE           = 500 / UNIT_TO_KILO; % Pa
%
%   Future efforts could be made to more accurately characterize the
%   performance of our tires.

    C_rr = 0.0017 .* exp(0.0054 .* speed); % Source: Ben Colby
    rr = C_rr * normalForce;
end