import types
import numpy as np
from scipy.interpolate import interp1d


def reactor_measurements(t, x, u, v, p, meas):
    # This function uses process variables (t, x, u, v) as inputs, as well as a namespace
    # describing the nature of the measurements, to generate a set of measured
    # values. The measured values are returned as time-series objects
    #
    # Process variables:
    #   t: time (scalar or vector)
    #   x: namespace of state variables
    #   u: namespace of exogeneous inputs
    #   v: namespace of intermediate dependent variables (not state variables)
    #   p: namespace of parameters
    #
    # The measurement namespace "meas" has a field "fields", which contains the
    # names of the different measurements.
    # Each type of measurement has the following properties:
    #   .func: lambda function with inputs t, x, u, v, p used to calculate
    #          measurement value using process variables as input
    #   .var:  Magnitude of noise variance (assume Gaussian noise)
    #   .T:    Measurement period (T = 1/frequency)
    #   .D:    Measurement delay
    #
    # For example, a liquid level "h" may be given by x.V/p.A, with normally
    # distributed sensor noise with variance 0.1, measurement frequency of 2 Hz
    # and a measurement delay of 0.25 s. The corresponding structure would be:
    # meas.h =
    #     func: @(t,x,u,v) x.V / p.A
    #      var: 0.1
    #        T: 0.5
    #        D: 0.25

    # Calculate measurement values for each field in "meas"
    meas_dictionary = meas.__dict__
    y = {}
    for i in range(len(meas.fields)):
        current = meas_dictionary[meas.fields[i]]    # Current measurement
        values = current.func(t, x, u, v, p) \
               + current.var * np.random.normal(np.ones(t.size)) # Time-series values + noise
        times = np.array(range(0, t[-1], current.T)) # Measurement time points
        interp_func = interp1d(t, values) # Interpolate to measurement time-points

        # Create time-series object at measurement time-points, delayed by "D"
        y[meas.fields[i]] = types.SimpleNamespace(Time = times + current.D,
                                                  Data = interp_func(times))

    return types.SimpleNamespace(**y)