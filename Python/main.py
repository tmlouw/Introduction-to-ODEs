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
p.Nu = np.array([[0, 0], [-1, -1], [1, -2], [0, 1]])

#%% Define exogeneous variables
u = types.SimpleNamespace()
u.q1  = lambda t: 0.02
u.q2  = lambda t: 0.01 + 0.05 * (t > 400)
u.cA1 = lambda t: 1.50 + 0.50 * (t > 800)

y = np.zeros(t.size)
for i in range(1, t.size):
    y[i]  = 0.8*y[i-1] + 0.05*np.random.normal()

u.cB2 = interp1d(t, y + 2)

#%% Integrate ODE
x0 = np.empty(4)
x0[0] = 0.9     # m3, initial tank volume
x0[1] = 0.15    # mol/m3, initial concentration of A
x0[2] = 0.25    # mol/m3, initial concentration of A
x0[3] = 0.30    # mol/m3, initial concentration of A

x0 = np.array([0.9, 0.15, 0.25, 0.30])
sol = solve_ivp(lambda t, x: reactor_ode(t, x, u, p),
                [0, t[-1]], x0, t_eval = t)

V = sol.y[0]
nA = sol.y[1]
nB = sol.y[2]
nC = sol.y[3]
v = reactor_intermediate_variables(t, sol.y, u, p)

#%% Plot the solution to the problem
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(sol.t, v.h)

ax2 = fig.add_subplot(212)
ax2.plot(sol.t, v.cA3)
ax2.plot(sol.t, v.cB3)
ax2.plot(sol.t, v.cC3)
plt.show()
