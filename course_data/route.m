%% Route Manipulation:
function route(dirty_filename, clean_filename)
    % Name of file to read:
    %dirty_filename = "ASC2022_N_Dirty.txt";
    
    % Name of file to write to:
    %clean_filename = "ASC2022_N.csv"; 
    
    % Read in data from file:
    T = readtable(dirty_filename)
    
    % Get data from table columns:
    % NOTE: Some names (like slope___) had weird formatting from copying the
    % table, if needed you may need to remove the semi-colon in the above line
    % "T = readtable(dirty_filename);" ---> "T = readtable(dirty_filename)"
    % then you'll be able to see the actual filenames
    
    latitudes       = T.latitude;
    longitudes      = T.longitude;
    altitudes_feet  = T.altitude_ft_;
    slopes_percent  = T.slope___;
    distance_miles  = T.distance_mi_;
    intervals_ft    = T.distance_interval_ft_;
    
    % Now check if any have NaN's, all should be 0
    
    latitudes_nNan  = sum(numnan(latitudes));
    longitudes_nNan = sum(numnan(longitudes));
    altitudes_nNan  = sum(numnan(altitudes_feet));
    slopes_nNan     = sum(numnan(slopes_percent));
    distance_nNan   = sum(numnan(distance_miles));
    intervals_nNan  = sum(numnan(intervals_ft));
    
    % adjustments can be made here:
    % the first element of interval and slope are always NaN
    intervals_ft(1)     = 0;
    slopes_percent(1)    = slopes_percent(2) - intervals_ft(2) * ...
        ((slopes_percent(3) - slopes_percent(2))/(intervals_ft(3)));
    
    feet_to_meters      =  0.3048;
    miles_to_meters     = feet_to_meters * 5280;
    
    interval_meters     = intervals_ft .* feet_to_meters;
    distance_meters     = distance_miles .* miles_to_meters;
    altitude_meters     = altitudes_feet .* feet_to_meters;
    slopes_radian       = atan(slopes_percent / 100);
    
    % Stich back into new file
    
    data = table(...
                distance_meters, ...
                altitude_meters, ...
                slopes_radian,   ...
                interval_meters, ...
                latitudes,       ...
                longitudes,      ...
                altitudes_feet,  ...
                slopes_percent,  ...
                distance_miles,  ...
                intervals_ft ...
                );
    
    data.Properties.VariableNames = [...
                "Distance [m]",     ...
                "Altitude [m]",     ...
                "Slope [rad]",      ...
                "Interval [m]",     ...
                "Latitude [deg]",   ...
                "Longitude [deg]",  ...
                "Altitude [ft]",    ...
                "Slope [%]",        ...
                "Distance [mi]",    ...
                "Interval [ft]"     ...
                ];
    
    writetable(data, clean_filename);
    %plot(distance_miles, altitudes_feet)
end