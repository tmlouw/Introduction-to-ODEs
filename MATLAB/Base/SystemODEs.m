function dxdt = SystemODEs(t, x_vec, u, p)
% Calculate the time-derivative of all state variables
%
% The function requires the following process variables as inputs:
%   t: time (scalar or vector)
%   x: structure of state variables
%   u: structure of exogeneous inputs
%   p: structure of parameters

% Map state vector to structure and calculate intermediate variables
x = xV2xS(x_vec, p.state_fields);
v = CalculateIntermediates(t, x, u, p);

% Calculate state derivatives as structure
ddt.V  = u.q1(t) + u.q2(t) - v.q3 + v.S.V*x.V;
ddt.nA = v.nA1 - v.nA3 + v.S.nA*x.V;
ddt.nB = v.nB2 - v.nB3 + v.S.nB*x.V;
ddt.nC =       - v.nC3 + v.S.nC*x.V;

% Map state derivative structure to vector
dxdt = xS2xV(ddt, p.state_fields);



