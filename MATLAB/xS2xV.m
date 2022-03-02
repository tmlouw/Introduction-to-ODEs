function xV = xS2xV(xS, fields)
n = length(fields);
xV = zeros(n, 1);
for i = 1:n
    xV(i) = xS.(fields{i}); 
end
