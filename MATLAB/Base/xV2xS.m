function xS = xV2xS(xV, fields)
% Maps all elements in vector "xV" to the structure "xS", 
% using the elements in "fields" as field names.
n = length(fields);
for i = 1:n
    xS.(fields{i}) = xV(i,:);
end
