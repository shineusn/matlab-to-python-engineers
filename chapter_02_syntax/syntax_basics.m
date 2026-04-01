% Chapter 2: Core Syntax - MATLAB Examples
% Companion code for "From MATLAB to Python for Engineers and Scientists"

% Variables and arrays
a = 5;
b = [1, 2, 3, 4, 5];       % row vector
c = [1; 2; 3; 4; 5];       % column vector
M = [1 2; 3 4];             % 2x2 matrix

% Indexing (1-based in MATLAB)
first_element = b(1);       % = 1
last_element = b(end);      % = 5

% Loop
for i = 1:5
    disp(i)
end

% Function definition (save as separate .m file or use end keyword)
function result = square(x)
    result = x.^2;
end
