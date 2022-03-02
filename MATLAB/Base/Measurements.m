function y = Measurements(t, x, u, v, p, meas)
% This function uses process variables (t, x, u, v) as inputs, as well as a structure
% describing the nature of the measurements, to generate a set of measured
% values.
%
% Process variables:
%   t: time (scalar or vector)
%   x: structure of state variables
%   u: structure of exogeneous inputs
%   v: structure of intermediate dependent variables (not state variables)
%   p: structure of parameters
%
% The measurement structure "meas" has a field "fields", which contains the
% names of the different measurements. The properties of each different
% measurement can be accessed by "meas.(fields{i})" for i = 1, 2, 3, ...
% Each type of measurement has the following properties:
%   .func: Anonymous function with inputs @(t, x, u, v, p) used to calculate 
%          measurement value using process variables as input
%   .var:  Magnitude of noise variance (assume Gaussian noise)
%   .T:    Measurement period (T = 1/frequency)
%   .D:    Measurement delay
%
% For example, a liquid level "h" may be given by x.V/p.A, with normally
% distributed sensor noise with variance 0.1, measurement frequency of 2 Hz
% and a measurement delay of 0.25 s. The corresponding structure would be:
% meas.h = 
%     func: @(t,x,u,v) x.V / p.A
%      var: 0.1
%        T: 0.5
%        D: 0.25

% Calculate measurement values for each field in "meas"
for i = 1:length(meas.fields)
    current = meas.(meas.fields{i});    % Current measurement
    values = current.func(t, x, u, v) + current.var*randn(size(t)); % Time-series values + noise
    times = 0 : current.T : t(end); % Measurement time points
    interp_values = interp1(t, values, times); % Interpolate to measurement time-points
    
    % Create time-series object at measurement time-points, delayed by "D"
    y.(meas.fields{i}) = timeseries(interp_values, times + current.D); 
end