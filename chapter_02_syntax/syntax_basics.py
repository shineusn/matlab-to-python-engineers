# Chapter 2: Core Syntax - Python Examples
# Companion code for "From MATLAB to Python for Engineers and Scientists"

import numpy as np

# Variables and arrays
a = 5
b = np.array([1, 2, 3, 4, 5])    # row vector equivalent
c = np.array([[1],[2],[3],[4],[5]]) # column vector
M = np.array([[1, 2],[3, 4]])      # 2x2 matrix

# Indexing (0-based in Python — key difference from MATLAB!)
first_element = b[0]    # = 1  (note: index 0, not 1)
last_element = b[-1]    # = 5

# Loop
for i in range(1, 6):
    print(i)

# Function definition
def square(x):
    return x ** 2
