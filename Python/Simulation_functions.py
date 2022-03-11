import types
import numpy as np

def reactor_intermediate_variables(t, x, u, p):
    # Unpack vector
    V = x[0]
    nA = x[1]
    nB = x[2]
    nC = x[3]

    # Calculate intermediate values
    v = types.SimpleNamespace()
    v.cA3 = nA / V
    v.cB3 = nB / V
    v.cC3 = nC / V

    v.h = V / p.A
    v.q3 = p.cV*np.sqrt(np.abs(v.h))
    v.nA1 = u.q1(t)*u.cA1(t)
    v.nB2 = u.q2(t)*u.cB2(t)
    v.nA3 = v.q3   *v.cA3
    v.nB3 = v.q3   *v.cB3
    v.nC3 = v.q3   *v.cC3

    if type(t) == float:
        r = np.zeros([2, 1])
    else:
        r = np.zeros([2, t.size])

    r[0,:] = p.k1 *v.cA3
    r[1,:] = p.k2f*v.cA3*v.cB3**2 - p.k2r*v.cC3

    v.S = p.Nu.dot(r)

    return v

def reactor_ode(t, x, u, p):
    # Unpack vector
    V = x[0]
    nA = x[1]
    nB = x[2]
    nC = x[3]

    v = reactor_intermediate_variables(t, x, u, p)

    dV_dt  = u.q1(t) +  u.q2(t) - v.q3  + v.S[0]
    dnA_dt = v.nA1              - v.nA3 + v.S[1]
    dnB_dt =            v.nB2   - v.nB3 + v.S[2]
    dnC_dt =                    - v.nC3 + v.S[3]

    dx_dt = np.empty_like(x)
    dx_dt[0] = dV_dt
    dx_dt[1] = dnA_dt
    dx_dt[2] = dnB_dt
    dx_dt[3] = dnC_dt
    return dx_dt
