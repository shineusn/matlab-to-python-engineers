% ============================================================
% Chapter 3: Numerical Computing with NumPy and SciPy
% "From MATLAB to Python for Engineers and Scientists"
% MATLAB Reference Code
% ============================================================

%% 3.1 Array Creation and Properties
% ------------------------------------------------------------
% Basic array construction
v = [1, 2, 3, 4, 5];
M = [1, 2, 3; 4, 5, 6; 7, 8, 9];

% Properties
disp(size(M))       % [3, 3]
disp(size(M, 1))    % 3  — number of rows
disp(size(M, 2))    % 3  — number of columns
disp(numel(M))      % 9  — total number of elements
disp(ndims(M))      % 2  — number of dimensions

% Reshape
v_col = reshape(v, 5, 1);       % reshape to column vector
M2    = reshape(1:12, 3, 4);    % 3x4 matrix from range

% Flatten matrix to vector
flat = M(:);    % column vector, column-major order


%% 3.2 Array Operations and Broadcasting
% ------------------------------------------------------------
A = [1, 2, 3; 4, 5, 6];    % 2x3
s = 10;

% Scalar operations — applied to every element
A_scaled  = A * s;      % multiply all elements by 10
A_shifted = A + s;      % add 10 to all elements
A_sq      = A .^ 2;     % square every element

% Element-wise operations between arrays of same shape
B = [7, 8, 9; 10, 11, 12];
C = A .* B;     % element-wise multiply
D = A ./ B;     % element-wise divide

% Broadcasting (MATLAB R2016b+)
col_vec = [1; 2];       % 2x1
result  = A + col_vec;  % adds col_vec to each column of A
%   [1+1, 2+1, 3+1]     [2, 3, 4]
%   [4+2, 5+2, 6+2]  =  [6, 7, 8]

row_vec = [10, 20, 30]; % 1x3
result2 = A + row_vec;  % adds row_vec to each row of A


%% 3.3 Linear Algebra
% ------------------------------------------------------------
A = [2, 1; 5, 3];
b = [4; 7];

% Matrix inverse
A_inv = inv(A);

% Solve linear system Ax = b  (preferred over inv for numerical stability)
x = A \ b;          % backslash operator — fast and stable
disp(x)             % solution vector

% Verify: A*x should equal b
disp(A * x)

% Determinant
d = det(A);

% Eigenvalues and eigenvectors
[V, D] = eig(A);    % V = eigenvectors (columns), D = diagonal eigenvalues
eigenvalues = diag(D);

% Singular Value Decomposition
[U, S, V] = svd(A);

% Matrix norms
n1   = norm(A, 1);      % 1-norm
n2   = norm(A);         % 2-norm (default, spectral norm)
ninf = norm(A, inf);    % inf-norm
nf   = norm(A, 'fro');  % Frobenius norm

% Rank
r = rank(A);

% Trace
t = trace(A);


%% 3.4 Calculus: Integration and Differentiation
% ------------------------------------------------------------

% Numerical integration (quadrature)
f   = @(x) x.^2 + 2*x + 1;
result_int = integral(f, 0, 3);    % definite integral from 0 to 3
disp(result_int)    % 21.0

% Numerical differentiation (gradient)
x  = 0:0.1:2*pi;
y  = sin(x);
dy = gradient(y, x);   % dy/dx using central differences

% Trapezoidal integration on discrete data
area = trapz(x, y);


%% 3.5 Solving Differential Equations
% ------------------------------------------------------------

% Solve ODE: dy/dt = -2y,  y(0) = 1
odefun = @(t, y) -2 * y;
tspan  = [0, 5];
y0     = 1;

[t, y] = ode45(odefun, tspan, y0);

% Plot solution
figure;
plot(t, y, 'b-', 'LineWidth', 2)
xlabel('t'); ylabel('y(t)')
title('ODE Solution: dy/dt = -2y')
grid on


%% 3.6 Optimization
% ------------------------------------------------------------

% Minimize a scalar function
f_min    = @(x) (x - 3).^2 + 2;
[x_opt, fval] = fminbnd(f_min, 0, 10);
fprintf('Minimum at x = %.4f, f(x) = %.4f\n', x_opt, fval)

% Minimize a multivariate function (unconstrained)
f_multi  = @(x) (x(1) - 1).^2 + (x(2) - 2).^2;
x0       = [0, 0];
options  = optimset('Display', 'off');
[x_opt2, fval2] = fminsearch(f_multi, x0, options);

% Find root of a function: f(x) = x^3 - 2x - 5
f_root   = @(x) x.^3 - 2*x - 5;
x_root   = fzero(f_root, 2);
fprintf('Root at x = %.4f\n', x_root)


%% 3.7 Interpolation
% ------------------------------------------------------------
x_data = [0, 1, 2, 3, 4, 5];
y_data = [0, 1, 4, 9, 16, 25];   % y = x^2 data points

x_fine = linspace(0, 5, 100);

% Linear interpolation
y_linear = interp1(x_data, y_data, x_fine, 'linear');

% Cubic spline interpolation
y_spline = interp1(x_data, y_data, x_fine, 'spline');

% 2D interpolation
[X, Y]  = meshgrid(0:4, 0:4);
Z       = sin(X) .* cos(Y);
[Xq,Yq] = meshgrid(0:0.5:4, 0:0.5:4);
Zq      = interp2(X, Y, Z, Xq, Yq, 'linear');


%% 3.8 Statistics
% ------------------------------------------------------------
data = randn(1, 1000);  % 1000 random samples from N(0,1)

m    = mean(data);
med  = median(data);
s    = std(data);
v    = var(data);
mn   = min(data);
mx   = max(data);
p25  = prctile(data, 25);   % 25th percentile
p75  = prctile(data, 75);   % 75th percentile

% Correlation between two vectors
x = randn(1, 100);
y = 2*x + randn(1, 100);
r = corrcoef(x, y);     % returns 2x2 correlation matrix
fprintf('Correlation: %.4f\n', r(1,2))


%% 3.9 Real Simulation Example: Damped Oscillator
% ------------------------------------------------------------
% Simulate: m*x'' + c*x' + k*x = 0
% Parameters
m = 1.0;    % mass
c = 0.3;    % damping coefficient
k = 1.0;    % spring constant

% Convert to 1st order system: [x, v]' = [v, (-c*v - k*x)/m]
odefun = @(t, y) [y(2); (-c*y(2) - k*y(1)) / m];

tspan = [0, 30];
y0    = [1; 0];     % initial position=1, velocity=0

[t, sol] = ode45(odefun, tspan, y0);

figure;
plot(t, sol(:,1), 'b-', 'LineWidth', 2)
xlabel('Time (s)'); ylabel('Displacement')
title('Damped Oscillator')
grid on
