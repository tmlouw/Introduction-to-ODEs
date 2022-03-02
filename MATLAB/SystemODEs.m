function dxdt = SystemODEs(t, x_vec, u, p)
% Convert state vector to structure and calculate intermediate variables
x = xV2xS(x_vec, p.fields);
v = CalculateIntermediates(t, x, u, p);

% Calculate state derivatives
ddt.V  = u.q1(t) + u.q2(t) - v.q3 + v.S.V;
ddt.nA = v.nA1 - v.nA3 + v.S.nA;
ddt.nB = v.nB2 - v.nB3 + v.S.nB;
ddt.nC =       - v.nC3 + v.S.nC;

dxdt = xS2xV(ddt, p.fields);



