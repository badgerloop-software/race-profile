% Find Cd from viscosity (from airParams.m), density, and car constants.
% **TODO** make otherForces(v) a function that reads rolling resistance
% from car.slx

%%velocity should be taken from car.slx
velocity = 10 %placeholder
Re = (density * velocity * CAR_LENGTH) / viscosity;

%%example usage
Cd = calculateCd(Re)

function Cd = calculateCd(Re)
    global TOTAL_MASS FRONTAL_AREA CAR_LENGTH density viscosity
     %Calculate velocity from Re
    v = (Re * viscosity) / (density * CAR_LENGTH);
    
    
    % Calculate acceleration
    a = calculateAcceleration(v);
    
    
    % Calculate total force
    F_total = TOTAL_MASS * a;
    
    
    % Subtract other forces
    F_other = OtherForces(v);
    
    
    F_drag =-( F_total - F_other); %make sure F_drag is positive
    
    % Calculate Cd
    Cd = (2 * F_drag) / (density * v^2 * FRONTAL_AREA);

    %test
    fprintf('Calculated Cd: %.4f\n', Cd);
    fprintf('Calculated F_drag: %.2f N\n', F_drag);
    fprintf('Calculated other forces: %.2f N\n', F_other);
    fprintf('Calculated total force: %.2f N\n', F_total);
    fprintf('Calculated acceleration: %.2f m/s^2\n', a);
    fprintf('Calculated velocity: %.2f m/s\n', v);
end

function a = calculateAcceleration(v)
    % Calculate acceleration based on the curve-fit equation
    a = -0.000001 + 0.000012*v - 0.00025*v^2;
end

function F_other = OtherForces(v)
    F_other = 1; %placeholder. Should be rolling resistance from Car.slx
end