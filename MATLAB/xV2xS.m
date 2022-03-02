function xS = xV2xS(xV, fields)
n = length(fields);
for i = 1:n
    xS.(fields{i}) = xV(i,:);
end
