function v = CalculateIntermediates(t, x, u, p)
% Calculate intermediate process variables 
% (i.e. all variables which are neither exogeneous inputs 
%       nor state variables)
%
% The function requires the following process variables as inputs:
%   t: time (scalar or vector)
%   x: structure of state variables
%   u: structure of exogeneous inputs
%   p: structure of parameters

% Calculate concentrations in CSTR
v.cA3 = x.nA ./ x.V;   % mol/m3, concentration of A
v.cB3 = x.nB ./ x.V;   % mol/m3, concentration of B
v.cC3 = x.nC ./ x.V;   % mol/m3, concentration of C

% Calculate all flowrates into / out of CSTR
v.h  = x.V/p.A;            % m, liquid level in CSTR
v.q3 = p.cV*sqrt(v.h);     % m3/s, flowrate out of CSTR
v.nA1 = u.q1(t).*u.cA1(t); % mol/s, molar flowrate of A into CSTR
v.nB2 = u.q2(t).*u.cB2(t); % mol/s, molar flowrate of B into CSTR
v.nA3 = v.q3.*v.cA3;       % mol/s, molar flowrate of A out of CSTR
v.nB3 = v.q3.*v.cB3;       % mol/s, molar flowrate of B out of CSTR
v.nC3 = v.q3.*v.cC3;       % mol/s, molar flowrate of C out of CSTR

% Calculate reaction rates and source terms for each state variable
% This reaction vector must align with the stoichiometric
% coefficient matrix
r(1,:) = p.k1*v.cA3;        % mol/m3.s, reaction rate 1
r(2,:) = p.k2f*v.cA3.*v.cB3.^2 - p.k2r*v.cC3; % mol/m3.s, reaction rate 2

for i = 1:length(p.state_fields)
    v.S.(p.state_fields{i}) = p.Nu.(p.state_fields{i}) * r;
end