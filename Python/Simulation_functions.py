import types
import numpy as np

def reactor_ns2vec(x_ns, fields):
    # Convert the namespace of states to a vector,
    # sorted according to the order provided by "fields
    d = x_ns.__dict__               # Convert simple namespace to dictionary
    x_vec = np.zeros(len(fields))   # Initialize vector
    for i in range(len(fields)):
        x_vec[i] = d[fields[i]]     # Supply entries to vector
    return x_vec


def reactor_vec2ns(x_vec, fields):
    # Convert the state vector to a simple namespace,
    # sorted accroding to the order provided by "fields"
    # This code unpacks all elements in the vector into a dictionary,
    # then converts the dictionary into a simple namespace
    d = {fields[i]: x_vec[i] for i in range(len(fields))}
    return types.SimpleNamespace(**d)


def reactor_intermediate_variables(t, x, u, p):
    # Calculate intermediate values
    v = types.SimpleNamespace()
    v.cA3 = x.nA / x.V      # mol/m3, concentration of A
    v.cB3 = x.nB / x.V      # mol/m3, concentration of B
    v.cC3 = x.nC / x.V      # mol/m3, concentration of C

    v.h = x.V / p.A         # m, liquid level in tank
    v.q3 = p.cV*np.sqrt(np.abs(v.h))   # m3/s, outlet flowrate
    v.nA1 = u.q1(t)*u.cA1(t)           # mol/s, inlet molar flow rate of A
    v.nB2 = u.q2(t)*u.cB2(t)           # mol/s, inlet molar flow rate of B
    v.nA3 = v.q3   *v.cA3              # mol/s, outlet molar flow rate of A
    v.nB3 = v.q3   *v.cB3              # mol/s, outlet molar flow rate of B
    v.nC3 = v.q3   *v.cC3              # mol/s, outlet molar flow rate of C

    # Calculate reaction rates. Check if t is an array or a float
    if type(t) == float:
        r = np.zeros([2, 1])
    else:
        r = np.zeros([2, t.size])

    # Reaction rates in mol/m3.s
    r[0,:] = p.k1 *v.cA3
    r[1,:] = p.k2f*v.cA3*v.cB3**2 - p.k2r*v.cC3

    # Calculate source (generation / depletion terms) for each state variable,
    # in units of mol/m3.s. The code unpacks p.Nu into a dictionary, then creates
    # a new dictionary where each element is given by the matrix multiplication
    # of Nu*r. Finally, the dictionary is packed back into a namespace
    Nu = p.Nu.__dict__
    d = {p.fields[i]: Nu[p.fields[i]].dot(r) for i in range(len(p.fields))}
    v.S = types.SimpleNamespace(**d)

    return v

def reactor_ode(t, x_vec, u, p):
    # Unpack state vector into a namespace
    x = reactor_vec2ns(x_vec, p.fields)

    # Calculate intermediate variables
    v = reactor_intermediate_variables(t, x, u, p)

    # Calculate time derivatives for each state variable
    ddt = types.SimpleNamespace()
    ddt.V  = u.q1(t) +  u.q2(t) - v.q3  + v.S.V  *x.V
    ddt.nA = v.nA1              - v.nA3 + v.S.nA *x.V
    ddt.nB =            v.nB2   - v.nB3 + v.S.nB *x.V
    ddt.nC =                    - v.nC3 + v.S.nC *x.V

    # Convert namespace of time derivatives to vector and return
    return reactor_ns2vec(ddt, p.fields)
