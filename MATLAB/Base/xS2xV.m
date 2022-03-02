function xV = xS2xV(xS, fields)
% Map all elements in structure "xS" and indexed by "fields" 
% to the corresponding element in the vector "xV"
n = length(fields);
xV = zeros(n, length(xS.(fields{1})));
for i = 1:n
    xV(i,:) = xS.(fields{i}); 
end
