# ============================================================
# Chapter 3: Numerical Computing with NumPy and SciPy
# "From MATLAB to Python for Engineers and Scientists"
# Python Reference Code
# ============================================================

import numpy as np
import scipy.linalg as la
import scipy.integrate as integrate
import scipy.optimize as optimize
import scipy.interpolate as interpolate
import scipy.stats as stats
import matplotlib.pyplot as plt


# ============================================================
# 3.1 Array Creation and Properties
# ============================================================

v = np.array([1, 2, 3, 4, 5])
M = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

# Properties
print(M.shape)          # (3, 3)     — MATLAB: size(M)
print(M.shape[0])       # 3          — MATLAB: size(M,1)  rows
print(M.shape[1])       # 3          — MATLAB: size(M,2)  columns
print(M.size)           # 9          — MATLAB: numel(M)
print(M.ndim)           # 2          — MATLAB: ndims(M)
print(M.dtype)          # int64      — MATLAB: class(M)

# Reshape
v_col = v.reshape(5, 1)             # MATLAB: reshape(v,5,1)
M2    = np.arange(1, 13).reshape(3, 4)  # MATLAB: reshape(1:12,3,4)

# Flatten  — two options
flat_c = M.flatten()    # copy,  row-major (C order) by default
flat_v = M.ravel()      # view,  faster, no copy

# *** Key difference: NumPy flatten is ROW-major (C order) ***
# MATLAB's M(:) flattens COLUMN-major (Fortran order)
# To match MATLAB behavior:
flat_matlab_style = M.flatten(order='F')  # column-major, matches MATLAB M(:)


# ============================================================
# 3.2 Array Operations and Broadcasting
# ============================================================

A = np.array([[1, 2, 3],
              [4, 5, 6]])   # shape (2,3)
s = 10

# Scalar operations — identical syntax to MATLAB
A_scaled  = A * s       # MATLAB: A * s
A_shifted = A + s       # MATLAB: A + s
A_sq      = A ** 2      # MATLAB: A .^ 2

# Element-wise between same-shape arrays
B = np.array([[7, 8, 9],
              [10, 11, 12]])
C = A * B               # MATLAB: A .* B  — NOTE: * is element-wise in NumPy!
D = A / B               # MATLAB: A ./ B

# Broadcasting — NumPy handles this more naturally than MATLAB
col_vec = np.array([[1], [2]])  # shape (2,1)
result  = A + col_vec           # broadcasts across columns
#   [[1+1, 2+1, 3+1],     [[2, 3, 4],
#    [4+2, 5+2, 6+2]]  =   [6, 7, 8]]

row_vec = np.array([10, 20, 30])  # shape (3,)
result2 = A + row_vec             # broadcasts across rows — MATLAB: A + row_vec

# *** Broadcasting trap: shape matters ***
# (2,3) + (3,)   → works  (row_vec broadcast across rows)
# (2,3) + (2,)   → ERROR  (ambiguous — use reshape to be explicit)
# (2,3) + (2,1)  → works  (col_vec broadcast across columns)


# ============================================================
# 3.3 Linear Algebra
# ============================================================

A = np.array([[2., 1.],
              [5., 3.]])
b = np.array([4., 7.])

# Matrix inverse
A_inv = np.linalg.inv(A)            # MATLAB: inv(A)

# Solve linear system Ax = b  (ALWAYS prefer this over inv)
x = np.linalg.solve(A, b)          # MATLAB: A \ b
print("Solution:", x)

# Verify
print("Residual:", np.allclose(A @ x, b))   # should be True

# *** Important: Python has no backslash operator \  ***
# MATLAB's  x = A \ b  becomes  x = np.linalg.solve(A, b)
# Never use  x = inv(A) @ b  — it's slower and less numerically stable

# Determinant
d = np.linalg.det(A)                # MATLAB: det(A)

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)   # MATLAB: [V,D] = eig(A)
# Note: MATLAB returns eigenvectors as columns (same as NumPy)
# MATLAB returns eigenvalues in diagonal matrix D — NumPy returns 1D array

# Singular Value Decomposition
U, s_vals, Vh = np.linalg.svd(A)   # MATLAB: [U,S,V] = svd(A)
# *** Trap: NumPy returns Vh (V-transpose), not V ***
# To get V as in MATLAB: V = Vh.T

# Matrix norms
n1   = np.linalg.norm(A, 1)        # MATLAB: norm(A,1)
n2   = np.linalg.norm(A)           # MATLAB: norm(A)    spectral norm
ninf = np.linalg.norm(A, np.inf)   # MATLAB: norm(A,inf)
nf   = np.linalg.norm(A, 'fro')    # MATLAB: norm(A,'fro')

# Rank and trace
r = np.linalg.matrix_rank(A)       # MATLAB: rank(A)
t = np.trace(A)                     # MATLAB: trace(A)


# ============================================================
# 3.4 Calculus: Integration and Differentiation
# ============================================================

# Numerical integration
def f(x):
    return x**2 + 2*x + 1

result_int, error = integrate.quad(f, 0, 3)    # MATLAB: integral(f,0,3)
print(f"Integral = {result_int:.4f}")           # 21.0

# integrate.quad returns (value, error_estimate) — unpack both
# MATLAB integral() returns only the value

# Numerical gradient on discrete data
x  = np.linspace(0, 2*np.pi, 100)
y  = np.sin(x)
dy = np.gradient(y, x)              # MATLAB: gradient(y,x)

# Trapezoidal integration on discrete data
area = np.trapz(y, x)               # MATLAB: trapz(x,y)
# *** Trap: argument order is REVERSED ***
# MATLAB: trapz(x, y)
# NumPy:  np.trapz(y, x)


# ============================================================
# 3.5 Solving Differential Equations
# ============================================================

# Solve ODE: dy/dt = -2y,  y(0) = 1
def odefun(t, y):
    return -2 * y           # MATLAB: @(t,y) -2*y

tspan = (0, 5)              # MATLAB: [0, 5]
y0    = [1.0]               # MATLAB: 1  (must be list/array in Python)

sol = integrate.solve_ivp(odefun, tspan, y0,
                           dense_output=True,
                           max_step=0.1)    # MATLAB: ode45(odefun,tspan,y0)

t = sol.t
y = sol.y[0]

# *** Interface difference ***
# MATLAB: [t, y] = ode45(odefun, tspan, y0)
# Python:  sol = solve_ivp(...)  then  t=sol.t, y=sol.y[0]
# solve_ivp returns a Bunch object with multiple fields

plt.figure(figsize=(8, 4))
plt.plot(t, y, 'b-', linewidth=2)
plt.xlabel('t'); plt.ylabel('y(t)')
plt.title('ODE Solution: dy/dt = -2y')
plt.grid(True)
plt.tight_layout()
plt.savefig('ode_solution.png', dpi=150)
plt.show()


# ============================================================
# 3.6 Optimization
# ============================================================

# Minimize scalar function
def f_min(x):
    return (x - 3)**2 + 2

result = optimize.minimize_scalar(f_min, bounds=(0, 10), method='bounded')
print(f"Minimum at x = {result.x:.4f}, f(x) = {result.fun:.4f}")
# MATLAB: [x_opt, fval] = fminbnd(f_min, 0, 10)

# Minimize multivariate function
def f_multi(x):
    return (x[0] - 1)**2 + (x[1] - 2)**2

x0     = [0.0, 0.0]
result2 = optimize.minimize(f_multi, x0, method='Nelder-Mead')
print(f"Optimal: {result2.x}")
# MATLAB: fminsearch(f_multi, x0)

# Find root of a function: f(x) = x^3 - 2x - 5
def f_root(x):
    return x**3 - 2*x - 5

x_root = optimize.brentq(f_root, 1, 3)     # MATLAB: fzero(f_root, 2)
print(f"Root at x = {x_root:.4f}")


# ============================================================
# 3.7 Interpolation
# ============================================================

x_data = np.array([0., 1., 2., 3., 4., 5.])
y_data = np.array([0., 1., 4., 9., 16., 25.])  # y = x^2 samples

x_fine = np.linspace(0, 5, 100)

# Linear interpolation
f_linear = interpolate.interp1d(x_data, y_data, kind='linear')
y_linear = f_linear(x_fine)           # MATLAB: interp1(x,y,xq,'linear')

# Cubic spline
f_spline = interpolate.interp1d(x_data, y_data, kind='cubic')
y_spline = f_spline(x_fine)           # MATLAB: interp1(x,y,xq,'spline')

# *** Workflow difference ***
# MATLAB: y_new = interp1(x, y, x_new, 'linear')  — one step
# Python: first create interpolator, then call it — two steps
# This is more flexible (reuse the same interpolator many times)

# 2D interpolation
x2d = np.arange(0, 5)
y2d = np.arange(0, 5)
X, Y = np.meshgrid(x2d, y2d)
Z    = np.sin(X) * np.cos(Y)

f2d  = interpolate.RegularGridInterpolator((y2d, x2d), Z)
xq, yq = np.meshgrid(np.arange(0, 4.5, 0.5), np.arange(0, 4.5, 0.5))
pts  = np.column_stack([yq.ravel(), xq.ravel()])
Zq   = f2d(pts).reshape(xq.shape)     # MATLAB: interp2(X,Y,Z,Xq,Yq)


# ============================================================
# 3.8 Statistics
# ============================================================

rng  = np.random.default_rng(seed=42)   # reproducible random numbers
data = rng.standard_normal(1000)         # MATLAB: randn(1,1000)

m    = np.mean(data)                     # MATLAB: mean(data)
med  = np.median(data)                   # MATLAB: median(data)
s    = np.std(data, ddof=1)             # MATLAB: std(data)
v    = np.var(data, ddof=1)             # MATLAB: var(data)
mn   = np.min(data)                      # MATLAB: min(data)
mx   = np.max(data)                      # MATLAB: max(data)
p25  = np.percentile(data, 25)           # MATLAB: prctile(data,25)
p75  = np.percentile(data, 75)           # MATLAB: prctile(data,75)

# *** Important: ddof=1 for sample std/var (matches MATLAB default) ***
# np.std(data)         uses ddof=0 (population std) — NOT the MATLAB default
# np.std(data, ddof=1) uses ddof=1 (sample std)     — matches MATLAB std()

# Correlation
x_corr = rng.standard_normal(100)
y_corr = 2 * x_corr + rng.standard_normal(100)
r, p_value = stats.pearsonr(x_corr, y_corr)    # MATLAB: corrcoef(x,y)
print(f"Correlation: {r:.4f},  p-value: {p_value:.4f}")
# MATLAB corrcoef returns a 2x2 matrix — stats.pearsonr returns (r, p) directly


# ============================================================
# 3.9 Real Simulation Example: Damped Oscillator
# ============================================================
# Simulate: m*x'' + c*x' + k*x = 0
# Convert to 1st order system: state = [position, velocity]

m = 1.0     # mass
c = 0.3     # damping coefficient
k = 1.0     # spring constant

def damped_oscillator(t, state):
    x, v = state
    dxdt = v
    dvdt = (-c * v - k * x) / m
    return [dxdt, dvdt]

tspan = (0, 30)
y0    = [1.0, 0.0]      # initial position=1, velocity=0

sol = integrate.solve_ivp(damped_oscillator, tspan, y0,
                           max_step=0.05,
                           dense_output=True)

t   = sol.t
pos = sol.y[0]      # position
vel = sol.y[1]      # velocity

plt.figure(figsize=(10, 4))
plt.plot(t, pos, 'b-', linewidth=2, label='Position')
plt.plot(t, vel, 'r--', linewidth=1.5, label='Velocity')
plt.xlabel('Time (s)'); plt.ylabel('Amplitude')
plt.title('Damped Oscillator Simulation')
plt.legend(); plt.grid(True)
plt.tight_layout()
plt.savefig('damped_oscillator.png', dpi=150)
plt.show()


# ============================================================
# Chapter 3 Summary: Key Differences to Remember
# ============================================================
#
# 1. MATRIX MULTIPLY: A @ B  not  A * B
#    A * B in NumPy is always element-wise.
#
# 2. LINEAR SOLVE: np.linalg.solve(A, b)  replaces  A \ b
#    Never use inv(A) @ b — slower and less stable.
#
# 3. SVD returns Vh (V-transpose): V = Vh.T to match MATLAB.
#
# 4. trapz argument order is REVERSED:
#    MATLAB: trapz(x, y)  →  Python: np.trapz(y, x)
#
# 5. std/var use ddof=1 to match MATLAB:
#    np.std(data, ddof=1)  not  np.std(data)
#
# 6. solve_ivp replaces ode45 but returns an object, not [t, y].
#    Access results via sol.t and sol.y[row_index].
