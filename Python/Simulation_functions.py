import numpy as np


def ode_motion(t, x):
    v = x[0]
    s = x[1]
    k = 1
    m = 1000
    F = -k * s
    dvdt = F / m
    dsdt = v

    dxdt = np.array([dvdt, dsdt])
    return dxdt
