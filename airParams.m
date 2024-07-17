function [density, viscosity] = airParams(temperature, pressure, humidity)
%AIRPARAMS Summary of this function goes here
%   Detailed explanation goes here

% Convert Units
hecto       = 100;              % Solcast gives pressures in hPa
pressure    = pressure * hecto; % Convert hPa -> Pa
tempK       = temperature + 273.15; % Convert C -> K

% Useful values
R       = 8.314462; % J/(mol K), gas constant
MW_da   = 28.9647;  % g/mol, molecular weight of dry air
MW_v    = 18.01528; % g/mol, molecular weight of vapor
R_da    = R / MW_da;% J/(g K), specific gas constant for dry air
R_v     = R / MW_v; % 

%% Density calculations

% Find the saturation pressure of the vapor
% A high accuracy fit is given in 
% "Huang, J., 2018: A Simple Accurate Formula for Calculating Saturation 
% Vapor Pressure of Water and Ice. J. Appl. Meteor. Climatol., 57, 
% 1265–1272, https://doi.org/10.1175/JAMC-D-17-0334.1."
% For a simpler model one can use the magnus formula

if temperature > 0
    numerator   = exp(34.494 - (4924.99 ./ (temperature + 237.1)));
    denominator = (temperature + 105).^1.57;
    Psat        = numerator ./ denominator;
else
    numerator   = exp(43.494 - (6545.8 / (temperature + 278)));
    denominator = (temperature + 868).^2;
    Psat        = numerator ./ denominator;
end


Pvapor = Psat * humidity;       % Partial pressure of vapor
Pdryair= pressure - Pvapor;     % Partial pressure of dry air
w = (MW_v/MW_da) * Pvapor / Pdryair; % Humidity ratio

mf_da = 1 / (1 + w);    % mass fraction of dry air
mf_v  = w / (1 + w);    % mass fraction of vapor

rho_da = Pdryair / (R_da * tempK);
rho_v = Pvapor / (R_v * tempK);

density = rho_da + rho_v;
density = density / 1000; % convert to kg m^-3

% alternative method
% R_avg = mf_da * R_da + mf_v * R_v;
% rho2 = pressure / (R_avg * tempK);

%% Viscosity calculations

% Calculate the viscosity of air and vapor
% data was exported from EES using a function call viscosity(H2O,T=T) or
% viscosity(Air,T=T) temperatures are in celsius, viscosities in kg/(m-s)
tempCorrelationVals = [-40, -32.86, -25.71, -18.57, -11.43, -4.286, 2.857, ...
                        10, 17.14, 24.29, 31.43, 38.57, 45.71, 52.86, 60];

vaporViscCorrelation = [0.000007536, 0.000007787, 0.000008039, 0.000008292, ...
                        0.000008546, 0.000008802, 0.000009059, 0.000009317, ...
                        0.000009576, 0.000009836, 0.0000101, 0.00001036, ...
                        0.00001062, 0.00001089, 0.00001115];

airViscCorrelation  = [0.00001527, 0.00001564, 0.00001601, 0.00001637, ...
                       0.00001673, 0.00001708, 0.00001743, 0.00001778, ...
                       0.00001812, 0.00001845, 0.00001879, 0.00001912, ...
                       0.00001944, 0.00001976, 0.00002008];

muVapor = interp1(tempCorrelationVals, vaporViscCorrelation, temperature);
muAir   = interp1(tempCorrelationVals, airViscCorrelation, temperature);

molarMassMixture = mf_da * MW_da + mf_v * MW_v;
moleFracAir = mf_da * MW_da / molarMassMixture;
moleFracVap = mf_v * MW_v / molarMassMixture;

% weighted average:
viscosity = muAir * moleFracAir + muVapor * moleFracVap;

%% FUTURE WORK:
% Instead of a weighted average, use a more accurate method (such as wilkes
% mixture rule) to find the viscosity of the mixture

end