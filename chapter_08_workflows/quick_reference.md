# MATLAB ↔ Python Quick Reference
### "From MATLAB to Python for Engineers and Scientists"
### Companion repository: github.com/shineusn/matlab-to-python-engineers

---

## Arrays and Matrices

| Operation | MATLAB | Python (NumPy) |
|---|---|---|
| Create row vector | `a = [1, 2, 3]` | `a = np.array([1, 2, 3])` |
| Create column vector | `a = [1; 2; 3]` | `a = np.array([[1],[2],[3]])` |
| Create matrix | `A = [1 2; 3 4]` | `A = np.array([[1,2],[3,4]])` |
| Zeros matrix | `zeros(3, 3)` | `np.zeros((3, 3))` |
| Ones matrix | `ones(3, 3)` | `np.ones((3, 3))` |
| Identity matrix | `eye(3)` | `np.eye(3)` |
| Random matrix | `rand(3, 3)` | `np.random.rand(3, 3)` |
| Range vector | `1:10` | `np.arange(1, 11)` |
| Linspace | `linspace(0, 1, 5)` | `np.linspace(0, 1, 5)` |
| Array size | `size(A)` | `A.shape` |
| Rows | `size(A, 1)` | `A.shape[0]` |
| Columns | `size(A, 2)` | `A.shape[1]` |
| Total elements | `numel(A)` | `A.size` |
| Reshape | `reshape(A, 3, 4)` | `A.reshape(3, 4)` |
| Flatten (col-major) | `A(:)` | `A.flatten(order='F')` |
| Flatten (row-major) | *(not default)* | `A.flatten()` |
| Transpose | `A'` | `A.T` |
| Data type | `class(A)` | `A.dtype` |
| Convert to float | `double(A)` | `A.astype(np.float64)` |
| Convert to int | `int32(A)` | `A.astype(np.int32)` |

---

## Indexing ← Most Important Section

| Operation | MATLAB | Python |
|---|---|---|
| First element | `v(1)` | `v[0]` |
| Last element | `v(end)` | `v[-1]` |
| Second to last | `v(end-1)` | `v[-2]` |
| Slice (elements 2–4) | `v(2:4)` → 3 elements | `v[1:4]` → 3 elements |
| Every other element | `v(1:2:end)` | `v[::2]` |
| Reverse | `v(end:-1:1)` | `v[::-1]` |
| Matrix element | `A(i, j)` | `A[i-1, j-1]` |
| Entire row | `A(2, :)` | `A[1, :]` |
| Entire column | `A(:, 3)` | `A[:, 2]` |
| Submatrix | `A(1:2, 1:2)` | `A[0:2, 0:2]` |
| Boolean indexing | `v(v > 5)` | `v[v > 5]` |

> **Rule:** Subtract 1 from every MATLAB index. Python's slice end is exclusive.

---

## Arithmetic Operators

| Operation | MATLAB | Python (NumPy) |
|---|---|---|
| Matrix multiply | `A * B` | `A @ B` |
| Element-wise multiply | `A .* B` | `A * B` |
| Element-wise divide | `A ./ B` | `A / B` |
| Element-wise power | `A .^ n` | `A ** n` |
| Linear solve Ax=b | `A \ b` | `np.linalg.solve(A, b)` |
| Add scalar | `A + 5` | `A + 5` |
| Logical AND | `A & B` or `&&` | `A & B` (arrays) / `and` (scalars) |
| Logical OR | `A \| B` or `\|\|` | `A \| B` (arrays) / `or` (scalars) |

---

## Linear Algebra

| Operation | MATLAB | Python |
|---|---|---|
| Inverse | `inv(A)` | `np.linalg.inv(A)` |
| Determinant | `det(A)` | `np.linalg.det(A)` |
| Eigenvalues | `[V, D] = eig(A)` | `vals, vecs = np.linalg.eig(A)` |
| SVD | `[U, S, V] = svd(A)` | `U, s, Vh = np.linalg.svd(A)` — note Vh! |
| Rank | `rank(A)` | `np.linalg.matrix_rank(A)` |
| Trace | `trace(A)` | `np.trace(A)` |
| Norm | `norm(A)` | `np.linalg.norm(A)` |
| Frobenius norm | `norm(A,'fro')` | `np.linalg.norm(A,'fro')` |

---

## Statistics

| Operation | MATLAB | Python |
|---|---|---|
| Mean | `mean(v)` | `np.mean(v)` |
| Median | `median(v)` | `np.median(v)` |
| Std (sample) | `std(v)` | `np.std(v, ddof=1)` |
| Variance (sample) | `var(v)` | `np.var(v, ddof=1)` |
| Min / Max | `min(v)` / `max(v)` | `np.min(v)` / `np.max(v)` |
| Percentile | `prctile(v, 25)` | `np.percentile(v, 25)` |
| Correlation | `corrcoef(x, y)` | `scipy.stats.pearsonr(x, y)` |
| Histogram | `histogram(v, 30)` | `np.histogram(v, bins=30)` |
| Sort | `sort(v)` | `np.sort(v)` |
| Sort indices | `[~, idx] = sort(v)` | `idx = np.argsort(v)` |
| Cumulative sum | `cumsum(v)` | `np.cumsum(v)` |

> **Note:** `np.std(v)` uses ddof=0 (population). Use `ddof=1` to match MATLAB.

---

## Calculus and Differential Equations

| Operation | MATLAB | Python |
|---|---|---|
| Numerical integration | `integral(f, a, b)` | `scipy.integrate.quad(f, a, b)` |
| Trapezoidal | `trapz(x, y)` | `np.trapz(y, x)` ← order reversed! |
| Gradient | `gradient(y, x)` | `np.gradient(y, x)` |
| Solve ODE | `[t,y] = ode45(f, tspan, y0)` | `sol = solve_ivp(f, tspan, y0)` |
| ODE result | `t, y` directly | `sol.t`, `sol.y[0]` |

---

## Signal Processing

| Operation | MATLAB | Python |
|---|---|---|
| FFT | `fft(x)` | `np.fft.fft(x)` |
| Inverse FFT | `ifft(x)` | `np.fft.ifft(x)` |
| Butterworth filter | `[b,a] = butter(n, Wn)` | `b, a = signal.butter(n, Wn)` |
| Apply filter (zero-phase) | `filtfilt(b, a, x)` | `signal.filtfilt(b, a, x)` |
| Apply filter (causal) | `filter(b, a, x)` | `signal.lfilter(b, a, x)` |
| FIR filter | `fir1(n, Wn)` | `signal.firwin(n+1, Wn)` |
| Welch PSD | `[pxx, f] = pwelch(x,...,Fs)` | `f, pxx = signal.welch(x, fs=Fs)` ← reversed! |
| Spectrogram | `spectrogram(x, win, ...)` | `f,t,S = signal.spectrogram(x, ...)` |
| Cross-correlation | `xcorr(x, y)` | `signal.correlate(x, y)` |
| Convolution | `conv(x, h, 'same')` | `signal.convolve(x, h, mode='same')` |
| Chirp | `chirp(t, f0, t1, f1)` | `signal.chirp(t, f0, t1, f1)` |
| Resample | `resample(x, p, q)` | `signal.resample(x, num)` |
| Downsample | `downsample(x, n)` | `signal.decimate(x, n)` |

---

## Image Processing

| Operation | MATLAB (Image Toolbox) | Python |
|---|---|---|
| Read image | `imread('img.jpg')` | `skimage.io.imread('img.jpg')` |
| Write image | `imwrite(img, 'out.png')` | `skimage.io.imsave('out.png', img)` |
| Show image | `imshow(img)` | `ax.imshow(img); plt.show()` |
| RGB to gray | `rgb2gray(img)` → uint8 | `skimage.color.rgb2gray(img)` → float! |
| Resize | `imresize(img, 0.5)` | `skimage.transform.rescale(img, 0.5)` |
| Gaussian blur | `imgaussfilt(img, s)` | `skimage.filters.gaussian(img, sigma=s)` |
| Median filter | `medfilt2(img, [5,5])` | `scipy.ndimage.median_filter(img, 5)` |
| Edge (Sobel) | `edge(img, 'Sobel')` | `skimage.filters.sobel(img)` |
| Edge (Canny) | `edge(img, 'Canny')` | `skimage.feature.canny(img)` |
| Threshold | `imbinarize(img)` | `img > skimage.filters.threshold_otsu(img)` |
| Erode | `imerode(bw, se)` | `skimage.morphology.binary_erosion(bw, se)` |
| Dilate | `imdilate(bw, se)` | `skimage.morphology.binary_dilation(bw, se)` |
| Fill holes | `imfill(bw,'holes')` | `scipy.ndimage.binary_fill_holes(bw)` |
| Label regions | `bwlabel(bw)` | `skimage.measure.label(bw)` |
| Region props | `regionprops(L)` | `skimage.measure.regionprops(L)` |
| Hist equalize | `histeq(img)` | `skimage.exposure.equalize_hist(img)` |

> **OpenCV note:** `cv2.imread` returns BGR, not RGB.
> Convert with `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`.

---

## Data Handling (pandas vs MATLAB table)

| Operation | MATLAB | Python (pandas) |
|---|---|---|
| Create table | `table(col1, col2, ...)` | `pd.DataFrame({'A': col1, ...})` |
| Read CSV | `readtable('f.csv')` | `pd.read_csv('f.csv')` |
| Write CSV | `writetable(T, 'f.csv')` | `df.to_csv('f.csv', index=False)` |
| Read Excel | `readtable('f.xlsx')` | `pd.read_excel('f.xlsx')` |
| Select column | `T.ColName` | `df['ColName']` or `df.ColName` |
| Select columns | `T(:,{'A','B'})` | `df[['A','B']]` |
| Filter rows | `T(T.A > 5, :)` | `df[df['A'] > 5]` |
| Multi-condition | `T(A>5 & B<3, :)` | `df[(df['A']>5) & (df['B']<3)]` |
| Add column | `T.NewCol = vals` | `df['NewCol'] = vals` |
| Drop column | `T.Col = []` | `df.drop(columns=['Col'])` |
| Sort | `sortrows(T,'Col')` | `df.sort_values('Col')` |
| Group + mean | `splitapply(@mean,...)` | `df.groupby('G')['V'].mean()` |
| Missing detect | `isnan(v)` | `df.isna()` |
| Drop missing | `v(~isnan(v))` | `df.dropna()` |
| Fill missing | `v(isnan(v)) = 0` | `df.fillna(0)` |
| Join tables | `innerjoin(T1,T2,...)` | `pd.merge(df1,df2,on='key')` |
| Head / tail | `head(T,5)` / `tail(T,5)` | `df.head(5)` / `df.tail(5)` |
| Summary stats | `summary(T)` | `df.describe()` |

---

## Visualization

| Operation | MATLAB | Python (matplotlib) |
|---|---|---|
| New figure | `figure` | `fig, ax = plt.subplots()` |
| Line plot | `plot(x, y)` | `ax.plot(x, y)` |
| Scatter | `scatter(x, y)` | `ax.scatter(x, y)` |
| Bar chart | `bar(x, y)` | `ax.bar(x, y)` |
| Histogram | `histogram(v, n)` | `ax.hist(v, bins=n)` |
| Heatmap | `imagesc(Z)` | `ax.imshow(Z, origin='lower')` |
| Contour (filled) | `contourf(X,Y,Z,n)` | `ax.contourf(X,Y,Z,n)` |
| Colorbar | `colorbar` | `plt.colorbar(im, ax=ax)` |
| Title | `title('...')` | `ax.set_title('...')` |
| X label | `xlabel('...')` | `ax.set_xlabel('...')` |
| Y label | `ylabel('...')` | `ax.set_ylabel('...')` |
| Axis limits | `xlim([a,b])` | `ax.set_xlim([a,b])` |
| Grid | `grid on` | `ax.grid(True)` |
| Legend | `legend('A','B')` | `ax.legend()` |
| Subplots | `subplot(2,2,1)` | `fig,axes = plt.subplots(2,2)` |
| Hold on | `hold on` | *(not needed — just call ax.plot again)* |
| Save figure | `saveas(fig,'f.png')` | `plt.savefig('f.png', dpi=300, bbox_inches='tight')` |
| Show | `(automatic)` | `plt.show()` |
| Semilogy | `semilogy(x,y)` | `ax.semilogy(x,y)` |

---

## File I/O

| Operation | MATLAB | Python |
|---|---|---|
| Save .mat | `save('f.mat','var')` | `scipy.io.savemat('f.mat',{'var':v})` |
| Load .mat | `load('f.mat')` | `scipy.io.loadmat('f.mat')` |
| Save array | *(use .mat)* | `np.save('f.npy', arr)` |
| Load array | *(use .mat)* | `np.load('f.npy')` |
| Save CSV | `writematrix(M,'f.csv')` | `np.savetxt('f.csv', M, delimiter=',')` |
| Load CSV (numeric) | `readmatrix('f.csv')` | `np.loadtxt('f.csv', delimiter=',')` |

---

## Control Flow

| Operation | MATLAB | Python |
|---|---|---|
| If/else | `if ... elseif ... else ... end` | `if ... elif ... else:` |
| For loop | `for i = 1:n ... end` | `for i in range(1, n+1):` |
| While loop | `while cond ... end` | `while cond:` |
| Try/catch | `try ... catch e ... end` | `try ... except Exception as e:` |
| Function def | `function out = f(x) ... end` | `def f(x): return out` |
| Anonymous fn | `f = @(x) x.^2` | `f = lambda x: x**2` |
| Comment | `% comment` | `# comment` |
| Print | `disp(x)` / `fprintf(...)` | `print(x)` / `print(f'...')` |
| String format | `sprintf('%d items', n)` | `f'{n} items'` |

---

*Last updated: 2026 — companion code at github.com/shineusn/matlab-to-python-engineers*
