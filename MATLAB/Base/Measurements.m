function y = Measurements(t, x, u, p, v, meas)

values.q1  = u.q1(t) + meas.q1.noise  *randn(size(t)); 
values.q2  = u.q2(t) + meas.q2.noise  *randn(size(t));
values.q3  = v.q3    + meas.q3.noise  *randn(size(t));
values.h   = v.h     + meas.h.noise   *randn(size(t));
values.cA3 = v.cA3   + meas.cA3.noise *randn(size(t));
values.cB3 = v.cB3   + meas.cB3.noise *randn(size(t));
values.cC3 = v.cC3   + meas.cC3.noise *randn(size(t));
    
for i = 1:length(meas.fields)
    times = 0 : meas.(meas.fields{i}).T : t(end);
    interp_values = interp1(t, values.(meas.fields{i}), times);
    y.(meas.fields{i}) = timeseries(interp_values, times);

end