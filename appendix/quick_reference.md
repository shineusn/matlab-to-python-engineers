# MATLAB ↔ Python Quick Reference

| Operation           | MATLAB                    | Python (NumPy)              |
|---------------------|---------------------------|-----------------------------|
| Create array        | `a = [1, 2, 3]`           | `a = np.array([1, 2, 3])`   |
| Matrix multiply     | `A * B`                   | `A @ B`                     |
| Element-wise mult   | `A .* B`                  | `A * B`                     |
| Array size          | `size(A)`                 | `A.shape`                   |
| Zeros matrix        | `zeros(3, 3)`             | `np.zeros((3, 3))`          |
| Ones matrix         | `ones(3, 3)`              | `np.ones((3, 3))`           |
| Index first element | `A(1)`                    | `A[0]`                      |
| Index last element  | `A(end)`                  | `A[-1]`                     |
| Transpose           | `A'`                      | `A.T`                       |
| Linear solve        | `A \ b`                   | `np.linalg.solve(A, b)`     |
| FFT                 | `fft(x)`                  | `np.fft.fft(x)`             |
| Plot                | `plot(x, y)`              | `plt.plot(x, y)`            |
| Save variable       | `save('file.mat', 'A')`   | `np.save('file.npy', A)`    |
| Load variable       | `load('file.mat')`        | `np.load('file.npy')`       |
| For loop range      | `for i = 1:10`            | `for i in range(1, 11):`    |
| Print               | `disp(x)`                 | `print(x)`                  |
| String format       | `sprintf('%d', x)`        | `f'{x}'`                    |
| Logical AND         | `&&` or `&`               | `and` or `&`                |
| Inline comment      | `% comment`               | `# comment`                 |
