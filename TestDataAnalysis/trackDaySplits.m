%% Data splitter for Telemetry Data
% Jacob Petrie

%% Establish Event Times

timeZone = "America/Chicago";
date = "2024-04-14";

driving= [% Begin Nishil Driving
          "15:30", "coasts";    
          "15:54", "floorIt";
          "15:56", "constSpeed";
          "15:59", "highSpeed";
          % Begin Mingcan Driving
          "16:25", "start";    
          "16:40", "coasts";
          "16:49", "Pi lost";
          "16:55", "coasts";
          "17:02", "Pi lost";
          "17:10", "coasts";
          "17:14", "Pi lost";
          "17:40", "coasts";
          "17:46", "CW coasts";
          "17:48", "fault";
          "17:50", "CW coasts";
          "17:58", "CW coasts";
          "18:00", "CW coasts";
          "18:26", "CW coasts";
          "18:30", "CW Const speed + coast"];

numEvents = length(driving(:,1));

% Create file for each event

for i = 1:numEvents

end



