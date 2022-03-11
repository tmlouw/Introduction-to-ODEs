import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from Simulation_functions import *

t = np.arange(0, 1200)
sol = solve_ivp(ode_motion, [0, t[-1]], [1, 0], t_eval = t)


plt.style.use('seaborn-poster')
plt.subplot(211)
plt.plot(sol.t, sol.y[0])
plt.subplot(212)
plt.plot(sol.t, sol.y[1])
plt.show()
