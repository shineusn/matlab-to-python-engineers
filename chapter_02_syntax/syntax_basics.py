# ============================================================
# Chapter 2: Core Syntax and Concepts
# "From MATLAB to Python for Engineers and Scientists"
# Python Reference Code
# ============================================================
# Run in Jupyter notebook (recommended) or any Python 3.11+ environment
# Install dependencies: pip install -r requirements.txt

import numpy as np


# ============================================================
# 2.1 Variables and Basic Types
# ============================================================

a = 5           # int  (MATLAB: always 'double' by default)
b = 3.14        # float
c = "hello"     # str  (MATLAB: use single quotes 'hello')
d = True        # bool (MATLAB: true — lowercase in MATLAB)

print(type(a))  # <class 'int'>
print(type(c))  # <class 'str'>

# Key difference: Python has distinct int and float types.
# MATLAB treats almost everything as double by default.


# ============================================================
# 2.2 Arrays and Matrices
# ============================================================

# NumPy is the MATLAB-equivalent for arrays and matrices.
# You must import it — Python has no built-in matrix type.

# Row vector equivalent
row = np.array([1, 2, 3, 4, 5])

# Column vector (2D array with shape (5,1))
col = np.array([[1], [2], [3], [4], [5]])

# 2D Matrix
M = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

# Construction functions — very similar to MATLAB
Z = np.zeros((3, 3))        # MATLAB: zeros(3,3)  — note the tuple!
O = np.ones((3, 3))         # MATLAB: ones(3,3)
I = np.eye(3)               # MATLAB: eye(3)
R = np.random.rand(3, 3)    # MATLAB: rand(3,3)
L = np.linspace(0, 1, 5)   # MATLAB: linspace(0,1,5)  — identical!
S = np.arange(0, 1.25, 0.25) # MATLAB: 0:0.25:1

# Common trap: np.zeros((3,3)) uses a TUPLE, not two arguments.
# np.zeros(3, 3) will raise an error — easy mistake coming from MATLAB.


# ============================================================
# 2.3 Indexing  ← THE MOST IMPORTANT DIFFERENCE
# ============================================================
#
# MATLAB starts at 1.  Python starts at 0.
#
# This is the hardest habit to break when switching from MATLAB.
# Even after months of Python, you will occasionally write v[1]
# when you mean v[0]. It is completely normal — everyone does it.
# The good news: you will get a wrong answer, not a crash,
# so the mistake is usually easy to spot.

v = np.array([10, 20, 30, 40, 50])

first   = v[0]      # 10  — MATLAB: v(1)
third   = v[2]      # 30  — MATLAB: v(3)
last    = v[-1]     # 50  — MATLAB: v(end)   negative index = from end
second_to_last = v[-2]  # 40  — MATLAB: v(end-1)

# Slicing  (start:stop — stop is EXCLUSIVE, unlike MATLAB)
sub1 = v[1:4]       # [20, 30, 40] — MATLAB: v(2:4)
                    # Python v[1:4] means indices 1, 2, 3 — NOT 4
sub2 = v[::2]       # [10, 30, 50] — MATLAB: v(1:2:end)  every other

# *** Common trap: off-by-one errors ***
# MATLAB v(2:4) → elements at positions 2,3,4 → 3 elements
# Python  v[2:4] → elements at positions 2,3   → 2 elements
# Python  v[1:4] → elements at positions 1,2,3 → same 3 elements as MATLAB v(2:4)

# 2D matrix indexing
M = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

element  = M[1, 2]      # 6   — MATLAB: M(2,3)  both row and col shift by 1
row1     = M[1, :]      # [4, 5, 6] — MATLAB: M(2,:)
col2     = M[:, 2]      # [3, 6, 9] — MATLAB: M(:,3)
submat   = M[0:2, 0:2]  # top-left 2x2 — MATLAB: M(1:2,1:2)


# ============================================================
# 2.4 Arithmetic Operations
# ============================================================

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

add   = A + B       # element-wise addition       — same as MATLAB
sub   = A - B       # element-wise subtraction    — same as MATLAB
mmul  = A @ B       # MATRIX multiplication       — MATLAB: A * B
emul  = A * B       # element-wise multiplication — MATLAB: A .* B
ediv  = A / B       # element-wise division       — MATLAB: A ./ B
epow  = A ** 2      # element-wise power          — MATLAB: A .^ 2
trans = A.T         # transpose                   — MATLAB: A'

# *** Critical trap: * means different things ***
# MATLAB:  A * B  → matrix multiplication
# Python:  A * B  → element-wise multiplication
# Python:  A @ B  → matrix multiplication  (use @ for matmul)
#
# This causes silent bugs — no error, just wrong numbers.
# Always double-check whether you need * or @ in Python.


# ============================================================
# 2.5 Control Flow
# ============================================================

# If / elif / else  (MATLAB: elseif → Python: elif)
x = 7
if x > 10:
    print("large")
elif x > 5:          # MATLAB: elseif  →  Python: elif
    print("medium")
else:
    print("small")

# Python uses INDENTATION to define blocks — no 'end' keyword.
# MATLAB uses 'end'. Forgetting indentation = syntax error.

# For loop
total = 0
for i in range(1, 6):   # range(1,6) → 1,2,3,4,5  (6 is excluded)
    total += i           # MATLAB: total = total + i
print(total)  # 15

# range(1, 6) in Python ≈ 1:5 in MATLAB — but watch the endpoint!
# MATLAB 1:5  → 1,2,3,4,5
# Python range(1,6) → 1,2,3,4,5  (must write 6 to include 5)

# While loop
n = 1
while n < 32:
    n *= 2
print(n)  # 32


# ============================================================
# 2.6 Functions
# ============================================================

# Functions are defined inline — no separate .m file needed.
# This is a big workflow improvement over MATLAB.

def my_add(a, b):
    return a + b

result = my_add(3, 4)   # 7

# Multiple return values (like MATLAB [out1, out2] = func(...))
def min_max(v):
    return np.min(v), np.max(v)

lo, hi = min_max(np.array([3, 1, 4, 1, 5, 9]))
# lo = 1, hi = 9

# Default argument values (not available in basic MATLAB)
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))           # Hello, Alice!
print(greet("Alice", "Hi"))     # Hi, Alice!


# ============================================================
# 2.7 File I/O
# ============================================================

# Save / load NumPy arrays
data = np.array([[1, 2, 3], [4, 5, 6]])
np.save("my_data.npy", data)            # MATLAB: save('my_data.mat','data')
loaded = np.load("my_data.npy")

# CSV files — use pandas (covered in Chapter 4)
import pandas as pd
df = pd.read_csv("data.csv")            # MATLAB: readtable('data.csv')
df.to_csv("output.csv", index=False)    # MATLAB: writetable(T,'output.csv')

# Load MATLAB .mat files directly into Python (no conversion needed!)
from scipy.io import loadmat
mat = loadmat("matlab_file.mat")        # keys are variable names


# ============================================================
# 2.8 String Operations
# ============================================================

s1 = "Hello"
s2 = "World"

joined   = s1 + " " + s2       # 'Hello World'  — MATLAB: [s1,' ',s2]
upper_s  = s1.upper()           # 'HELLO'        — MATLAB: upper(s1)
length   = len(s1)              # 5              — MATLAB: length(s1)
has_ell  = "ell" in s1          # True           — MATLAB: contains(s1,'ell')

# f-strings: Python's cleaner version of MATLAB's sprintf
name = "Alice"
age  = 30
msg  = f"Name: {name}, Age: {age}"  # MATLAB: sprintf('Name: %s, Age: %d',name,age)
print(msg)


# ============================================================
# Chapter 2 Summary: Key Differences to Remember
# ============================================================
#
# 1. INDEXING: Python starts at 0. MATLAB starts at 1.
#    This takes the longest to internalize. Be patient with yourself.
#
# 2. SLICING end is EXCLUSIVE: v[1:4] gives indices 1,2,3 — not 4.
#    MATLAB v(1:4) gives indices 1,2,3,4.
#
# 3. MATRIX MULTIPLY: use @ in Python, not *.
#    Python's * is always element-wise for NumPy arrays.
#
# 4. NO 'end' KEYWORD: Python uses indentation for code blocks.
#
# 5. FUNCTIONS IN SAME FILE: no need for separate .m files.
#
# 6. IMPORT REQUIRED: numpy, pandas, matplotlib must be imported.
#    Nothing is available by default unlike MATLAB's built-ins.