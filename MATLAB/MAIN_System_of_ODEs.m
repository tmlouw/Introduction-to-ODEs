%% System of ODEs: CSTR with two reactions
%  Tobi Louw, 2022-03-02
%  This code is used to illustrate the implementation of ODEs in MATLAB
clc
clear
clf

%% Define time space of interest
t = linspace(0, 1200);  % s, Time over which to perform integration

%% Define parameters
p.cV  = 0.045;  % m2.5/s, Outlet flowrate coefficient
p.A   = 2;      % m2, Cross-sectional area of reactor
p.k1  = 5.0e-2; % 1/s, Reaction 1 rate constant 
p.k2f = 2.5e+0; % m6/mol2.s, Reaction 2 forward rate constant
p.k2r = 5.0e-2; % 1/s, Reaction 2 reverse rate constant

% Matrix of stoichiometric coefficients
p.Nu = [ 0  0; ...  % Source term for V
        -1 -1; ...  % Source term for A
        +1 -2; ...  % Source term for B
         0 +1];     % Source term for C

%% Define exogeneous inputs
u.q1  = @(t) 0.02;  % m3/s, Inlet flowrate 1
u.q2  = @(t) 0.01 + 0.05*(t > 400);  % m3/s, Inlet flowrate 2
u.cA1 = @(t) 1.50 + 0.50*(t > 800);  % mol/m3, Inlet concentration A

y(1) = 0;
for i = 2:length(t)
    y(i) = 0.8*y(i-1) + 0.05*randn;
end
y = y + 2.0;
u.cB2 = griddedInterpolant(t, y);

%% Define measurement frequency and noise
% In each case, noise is normally distributed with variance given below
meas.fields = {'q1','q2','q3','h','cA3','cB3','cC3'};

meas.q1.noise  = 0.001;
meas.q2.noise  = 0.001;
meas.q3.noise  = 0.001;
meas.h.noise   = 0.1;
meas.cA3.noise = 0.02; 
meas.cB3.noise = 0.02;
meas.cC3.noise = 0.02;

meas.q1.T  = 1;
meas.q2.T  = 1;
meas.q3.T  = 1;
meas.h.T   = 5;
meas.cA3.T = 60; 
meas.cB3.T = 60;
meas.cC3.T = 60;

%% Define fields for state structure and initial conditions
p.fields = {'V', 'nA', 'nB', 'nC'};
x0.V = 0.9;      % m3, initial tank volume
x0.nA = 0.15;    % mol/m3, initial concentration of A
x0.nB = 0.25;    % mol/m3, initial concentration of A
x0.nC = 0.30;    % mol/m3, initial concentration of A
x0_vec = xS2xV(x0, p.fields);

%% Simulate system of ODEs
[~, x_vec] = ode45(@(t, x) SystemODEs(t, x, u, p), t, x0_vec);
x = xV2xS(x_vec', p.fields);
v = CalculateIntermediates(t, x, u, p);
y = Measurements(t, x, u, p, v, meas);
%% Plot results
tiledlayout flow
nexttile
% Plot true values
plot(t, v.h, 'LineWidth',2);

% Plot measurements
hold on
plot(y.h,'k.','MarkerSize', 8)
legend('h', 'Location','northwest')

nexttile
% Plot true values
plot(t, v.cA3, t, v.cB3, t, v.cC3, 'LineWidth', 2)


% Plot measurements
hold on
set(gca,'ColorOrderIndex',1)
plot(y.cA3,'.','MarkerSize',20)
plot(y.cB3,'.','MarkerSize',20)
plot(y.cC3,'.','MarkerSize',20)
legend('c_A', 'c_B', 'c_C','Location','northwest')
