%% System of ODEs: CSTR with two reactions
%  Tobi Louw, 2022-03-02
%  This code is used to illustrate the implementation of ODEs in MATLAB
%  The example system is a CSTR facilitating two reactions, described in
%  the accompanying PDF
clc
clear
clf

%% Define time region of interest
t = linspace(0, 1200);  % s, Time over which to perform integration

%% Define parameters
p.cV  = 0.045;  % m2.5/s, Outlet flowrate coefficient
p.A   = 2;      % m2, Cross-sectional area of reactor
p.k1  = 5.0e-2; % 1/s, Reaction 1 rate constant 
p.k2f = 2.5e+0; % m6/mol2.s, Reaction 2 forward rate constant
p.k2r = 5.0e-2; % 1/s, Reaction 2 reverse rate constant

% Matrix of stoichiometric coefficients for each state variable
p.Nu.V = [ 0  0];
p.Nu.nA = [-1 -1];
p.Nu.nB = [+1 -2];
p.Nu.nC = [ 0 +1];

%% Define exogeneous inputs
u.q1  = @(t) 0.02 + 0*t;             % m3/s, Inlet flowrate 1 (constant)
u.q2  = @(t) 0.01 + 0.05*(t > 400);  % m3/s, Inlet flowrate 2 (step-change)
u.cA1 = @(t) 1.50 + 0.50*(t > 800);  % mol/m3, Inlet concentration A (step-change)

% Concentration cB2 will vary stochastically
y(1) = 0;
for i = 2:length(t)
    y(i) = 0.8*y(i-1) + 0.05*randn;
end
y = y + 2.0;
u.cB2 = griddedInterpolant(t, y);

%% Define state structure and initial conditions
p.state_fields = {'V', 'nA', 'nB', 'nC'};   % Field names for each state
x0.V = 0.9;      % m3, initial tank volume
x0.nA = 0.15;    % mol, initial amount of A
x0.nB = 0.25;    % mol, initial amount of A
x0.nC = 0.30;    % mol, initial amount of A   
x0_vec = xS2xV(x0, p.state_fields);

%% Simulate system of ODEs
[~, x_vec] = ode45(@(t, x) SystemODEs(t, x, u, p), t, x0_vec);
x = xV2xS(x_vec', p.state_fields);
v = CalculateIntermediates(t, x, u, p);

%% Plot simulation results
tiledlayout flow
ax_height = nexttile;
plot(t, v.h, 'LineWidth',2);
legend('h','Location','northwest','FontSize',12);
xlabel('Time (s)','FontSize',12); 
ylabel('Liquid level (m)','FontSize',12);

ax_concentration = nexttile;
plot(t, v.cA3, t, v.cB3, t, v.cC3, 'LineWidth', 2)
legend('c_A', 'c_B', 'c_C','Location','northwest','FontSize',12)
xlabel('Time (s)','FontSize',12); 
ylabel('Concentration (mol/m3)','FontSize',12);


%% Define measurement noise, frequency and delay
% Create measurement structures. Type "help Measurements" for more information
meas.fields = {'q1','q2','q3','h','cA3','cB3','cC3'};

meas.q1  = struct('func', @(t, x, u, v, p) u.q1(t), 'var', 0.001, 'T', 1,  'D', 0);
meas.q2  = struct('func', @(t, x, u, v, p) u.q2(t), 'var', 0.001, 'T', 1,  'D', 0);
meas.q3  = struct('func', @(t, x, u, v, p) v.q3,    'var', 0.001, 'T', 1,  'D', 0);
meas.h   = struct('func', @(t, x, u, v, p) v.h,     'var', 0.1,   'T', 5,  'D', 2);
meas.cA3 = struct('func', @(t, x, u, v, p) v.cA3,   'var', 0.02,  'T', 60, 'D', 60);
meas.cB3 = struct('func', @(t, x, u, v, p) v.cB3,   'var', 0.02,  'T', 60, 'D', 60);
meas.cC3 = struct('func', @(t, x, u, v, p) v.cC3,   'var', 0.02,  'T', 60, 'D', 60);


% Record measurements
y = Measurements(t, x, u, v, p, meas);

%% Plot measurements
axes(ax_height)
hold on
plot(y.h,'k.','MarkerSize', 8)
legend('h', 'Location','northwest')

axes(ax_concentration)
hold on
set(gca,'ColorOrderIndex',1)
plot(y.cA3,'.','MarkerSize',20)
plot(y.cB3,'.','MarkerSize',20)
plot(y.cC3,'.','MarkerSize',20)
legend('c_A', 'c_B', 'c_C','Location','northwest')