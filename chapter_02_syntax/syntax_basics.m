% ============================================================
% Chapter 2: Core Syntax and Concepts
% "From MATLAB to Python for Engineers and Scientists"
% MATLAB Reference Code
% ============================================================
% Run each section independently using Ctrl+Enter (Cell Mode)
% or copy-paste into MATLAB Command Window


%% 2.1 Variables and Basic Types
% ------------------------------------------------------------
a = 5;              % integer-like scalar
b = 3.14;           % floating point
c = 'hello';        % character string
d = true;           % logical

disp(class(a))      % 'double' (MATLAB default numeric type)
disp(class(c))      % 'char'


%% 2.2 Arrays and Matrices
% ------------------------------------------------------------
% Row vector
row = [1, 2, 3, 4, 5];

% Column vector
col = [1; 2; 3; 4; 5];

% 2D Matrix
M = [1, 2, 3;
     4, 5, 6;
     7, 8, 9];

% Useful construction functions
Z = zeros(3, 3);        % 3x3 zeros
O = ones(3, 3);         % 3x3 ones
I = eye(3);             % 3x3 identity matrix
R = rand(3, 3);         % 3x3 random (uniform)
L = linspace(0, 1, 5); % 5 evenly spaced values from 0 to 1
S = 0:0.25:1;           % same result using step syntax


%% 2.3 Indexing
% ------------------------------------------------------------
% *** MATLAB INDEXING STARTS AT 1 ***
% This is the single biggest difference from Python.
% After years of MATLAB, switching to 0-based indexing
% takes real time to get used to — you WILL make this mistake.

v = [10, 20, 30, 40, 50];

first   = v(1);         % 10  — first element is index 1
third   = v(3);         % 30
last    = v(end);       % 50  — 'end' keyword for last element
second_to_last = v(end-1); % 40

% Slicing (ranges)
sub1 = v(2:4);          % [20, 30, 40] — indices 2 through 4
sub2 = v(1:2:end);      % [10, 30, 50] — every other element

% 2D matrix indexing
M = [1, 2, 3;
     4, 5, 6;
     7, 8, 9];

element  = M(2, 3);     % 6   — row 2, column 3
row2     = M(2, :);     % [4, 5, 6] — entire row 2
col3     = M(:, 3);     % [3; 6; 9] — entire column 3
submat   = M(1:2, 1:2); % top-left 2x2 submatrix


%% 2.4 Arithmetic Operations
% ------------------------------------------------------------
A = [1, 2; 3, 4];
B = [5, 6; 7, 8];

add   = A + B;      % element-wise addition
sub   = A - B;      % element-wise subtraction
mmul  = A * B;      % MATRIX multiplication (NOT element-wise)
emul  = A .* B;     % element-wise multiplication (note the dot)
ediv  = A ./ B;     % element-wise division
epow  = A .^ 2;     % element-wise power
trans = A';         % transpose


%% 2.5 Control Flow
% ------------------------------------------------------------

% If / elseif / else
x = 7;
if x > 10
    disp('large')
elseif x > 5
    disp('medium')
else
    disp('small')
end

% For loop (range)
total = 0;
for i = 1:5
    total = total + i;
end
disp(total)   % 15

% While loop
n = 1;
while n < 32
    n = n * 2;
end
disp(n)   % 32


%% 2.6 Functions
% ------------------------------------------------------------
% In MATLAB, functions are typically defined in separate .m files
% or at the end of a script (R2016b+)

% Calling a function
result = my_add(3, 4);  % = 7

% Function definition (place at end of script or in separate file)
function out = my_add(a, b)
    out = a + b;
end

% Function with multiple outputs
function [mn, mx] = min_max(v)
    mn = min(v);
    mx = max(v);
end

% Usage:
[lo, hi] = min_max([3, 1, 4, 1, 5, 9]);
% lo = 1, hi = 9


%% 2.7 File I/O
% ------------------------------------------------------------

% Save and load .mat files
data = [1, 2, 3; 4, 5, 6];
save('my_data.mat', 'data');
loaded = load('my_data.mat');
disp(loaded.data)

% Read CSV
T = readtable('data.csv');

% Write CSV
writetable(T, 'output.csv');


%% 2.8 String Operations
% ------------------------------------------------------------
s1 = 'Hello';
s2 = 'World';

joined  = [s1, ' ', s2];       % 'Hello World'  (concatenation)
upper_s = upper(s1);            % 'HELLO'
len     = length(s1);           % 5
has_ell = contains(s1, 'ell');  % true

% Formatted string (sprintf)
name = 'Alice';
age  = 30;
msg  = sprintf('Name: %s, Age: %d', name, age);
disp(msg)