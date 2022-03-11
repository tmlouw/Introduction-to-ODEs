#%% Clear and import
from IPython import get_ipython
get_ipython().run_line_magic('reset', '-f')

from Simulation_functions import *
import types
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

#%% Define time range and parameters
t = np.arange(0, 1200) # s, time over which to peform integration

p = types.SimpleNamespace()
p.cV  = 0.045  # m2.5/s, Outlet flowrate coefficient
p.A   = 2      # m2, Cross-sectional area of reactor
p.k1  = 5.0e-2 # 1/s, Reaction 1 rate constant
p.k2f = 2.5e+0 # m6/mol2.s, Reaction 2 forward rate constant
p.k2r = 5.0e-2 # 1/s, Reaction 2 reverse rate constant

# Matrix of stoichiometric coefficients for each state variable
p.Nu = types.SimpleNamespace(V  = np.array([ 0,  0]),
                             nA = np.array([-1, -1]),
                             nB = np.array([ 1, -2]),
                             nC = np.array([ 0,  1]))

#%% Define exogeneous variables
u = types.SimpleNamespace()
u.q1  = lambda t: 0.02
u.q2  = lambda t: 0.01 + 0.05 * (t > 400)
u.cA1 = lambda t: 1.50 + 0.50 * (t > 800)

y = np.zeros(t.size)
for i in range(1, t.size):
    y[i]  = 0.8*y[i-1] + 0.05*np.random.normal()

u.cB2 = interp1d(t, y + 2)

#%% Define state variables and integrate ODE
p.fields = ['V', 'nA', 'nB', 'nC']
x0 = types.SimpleNamespace(V = 0.9,     # m3, initial tank volume
                           nA = 0.15,   # mol, initial amount of A
                           nB = 0.25,   # mol, initial amount of A
                           nC = 0.30)   # mol, initial amount of A

x0_vec = reactor_ns2vec(x0, p.fields)
sol = solve_ivp(lambda t, x: reactor_ode(t, x, u, p),
                [0, t[-1]], x0_vec, t_eval = t)

x = reactor_vec2ns(sol.y, p.fields)
v = reactor_intermediate_variables(t, x, u, p)

#%% Plot the solution to the problem
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(sol.t, v.h)

ax2 = fig.add_subplot(212)
ax2.plot(sol.t, v.cA3)
ax2.plot(sol.t, v.cB3)
ax2.plot(sol.t, v.cC3)
plt.show()
