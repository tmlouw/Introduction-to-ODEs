#%% Clear and import required modules
from IPython import get_ipython
get_ipython().run_line_magic('reset', '-f')

from Simulation_functions import *
from Measurement_functions import *
import types
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

#%% Define time range and parameters
t = np.arange(0, 1200) # s, time over which to peform integration

p = types.SimpleNamespace(cV  = 0.045,  # m2.5/s, Outlet flowrate coefficient
                          A   = 2,      # m2, Cross-sectional area of reactor
                          k1  = 5.0e-2, # 1/s, Reaction 1 rate constant
                          k2f = 2.5e+0, # m6/mol2.s, Reaction 2 forward rate constant
                          k2r = 5.0e-2) # 1/s, Reaction 2 reverse rate constant

# Matrix of stoichiometric coefficients for each state variable
p.Nu = types.SimpleNamespace(V  = np.array([ 0,  0]),
                             nA = np.array([-1, -1]),
                             nB = np.array([ 1, -2]),
                             nC = np.array([ 0,  1]))

#%% Define exogeneous variables
u = types.SimpleNamespace(q1  = lambda t: 0.02,                    # m3/s, stream 1 flow rate
                          q2  = lambda t: 0.01 + 0.05 * (t > 400), # m3/s, stream 1 flow rate
                          cA1 = lambda t: 1.50 + 0.50 * (t > 800)) # mol/m3, stream 1 concentration

# Define the inlet concentration of B in stream 2 as an ARX sequence
y = np.zeros(t.size)
for i in range(1, t.size):
    y[i]  = 0.8*y[i-1] + 0.05*np.random.normal()

# Interpolate the ARX function to create a lambda function with time as input
u.cB2 = interp1d(t, y + 2)      # mol/m3, stream 2 concentration

#%% Define state variables, initial conditions and integrate ODE
p.fields = ['V', 'nA', 'nB', 'nC']
x0 = types.SimpleNamespace(V = 0.9,     # m3, initial tank volume
                           nA = 0.15,   # mol, initial amount of A
                           nB = 0.25,   # mol, initial amount of A
                           nC = 0.30)   # mol, initial amount of A

x0_vec = reactor_ns2vec(x0, p.fields)
sol = solve_ivp(lambda t, x: reactor_ode(t, x, u, p),
                [0, t[-1]], x0_vec, t_eval = t)

# Convert output state vector to state- and intermediate variable namespace
x = reactor_vec2ns(sol.y, p.fields)
v = reactor_intermediate_variables(t, x, u, p)


#%% Define measurement noise, frequency and delay
# Create measurement namespace.
meas = types.SimpleNamespace()
meas.q1  = types.SimpleNamespace(func = lambda t, x, u, v, p: u.q1(t),
                                 var = 0.001,
                                 T = 1,
                                 D = 0)
meas.q2  = types.SimpleNamespace(func = lambda t, x, u, v, p: u.q2(t),
                                 var = 0.001,
                                 T = 1,
                                 D = 0)
meas.q3  = types.SimpleNamespace(func = lambda t, x, u, v, p: v.q3,
                                 var = 0.001,
                                 T = 1,
                                 D = 0)
meas.h   = types.SimpleNamespace(func = lambda t, x, u, v, p: v.h,
                                 var = 0.1,
                                 T = 5,
                                 D = 2)
meas.cA3 = types.SimpleNamespace(func = lambda t, x, u, v, p: v.cA3,
                                 var = 0.02,
                                 T = 60,
                                 D = 60)
meas.cB3 = types.SimpleNamespace(func = lambda t, x, u, v, p: v.cB3,
                                 var = 0.02,
                                 T = 60,
                                 D = 60)
meas.cC3 = types.SimpleNamespace(func = lambda t, x, u, v, p: v.cC3,
                                 var = 0.02,
                                 T = 60,
                                 D = 60)
meas.fields = list(meas.__dict__.keys())

# Record measurements
y = reactor_measurements(t, x, u, v, p, meas)

#%% Plot the height, concentration, and measurements
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(t, v.h)

ax2 = fig.add_subplot(212)
ax2.plot(t, v.cA3)
ax2.plot(t, v.cB3)
ax2.plot(t, v.cC3)

ax1.plot(y.h.Time, y.h.Data, 'ko', ms = 2, mfc = 'C0', mew = 0.5)
ax2.plot(y.cA3.Time, y.cA3.Data, 'ko', ms = 4, mfc = 'C0', mew = 0.5)
ax2.plot(y.cB3.Time, y.cB3.Data, 'ko', ms = 4, mfc = 'C1', mew = 0.5)
ax2.plot(y.cC3.Time, y.cC3.Data, 'ko', ms = 4, mfc = 'C2', mew = 0.5)

ax1.set_ylabel('Liquid level (m)')
ax2.set_ylabel('Concentration (mol/m3)')
ax2.set_xlabel('Time (s)')


plt.show()
