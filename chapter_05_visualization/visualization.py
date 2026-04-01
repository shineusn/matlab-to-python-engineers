# ============================================================
# Chapter 5: Visualization – From MATLAB Plots to Python Figures
# "From MATLAB to Python for Engineers and Scientists"
# Python Reference Code
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd


# ============================================================
# 5.1 Basic Line and Scatter Plots
# ============================================================

x  = np.linspace(0, 2 * np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Simple line plot
fig, ax = plt.subplots()
ax.plot(x, y1)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Sine Wave')
ax.grid(True)
plt.tight_layout()
plt.savefig('sine_basic.png', dpi=150)
plt.show()

# *** Two interfaces: pyplot (MATLAB-style) vs OOP (recommended) ***
#
# pyplot style — looks like MATLAB, fine for quick exploration:
#   plt.plot(x, y)
#   plt.xlabel('x')
#   plt.title('...')
#   plt.show()
#
# OOP style — recommended for all real work:
#   fig, ax = plt.subplots()
#   ax.plot(x, y)
#   ax.set_xlabel('x')
#   ax.set_title('...')
#   plt.show()
#
# The OOP style gives you explicit control over each axes object,
# which is essential when working with subplots or multiple figures.
# MATLAB users often start with pyplot (familiar feel) then switch
# to OOP once they need more control.

# Multiple lines — no hold on/off needed, just call plot() again
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y1, 'b-',  linewidth=2, label='sin(x)')   # MATLAB: 'b-','LineWidth',2
ax.plot(x, y2, 'r--', linewidth=2, label='cos(x)')
ax.set_xlabel('x');  ax.set_ylabel('y')
ax.set_title('Sine and Cosine')
ax.legend(loc='best')
ax.grid(True)
plt.tight_layout()
plt.savefig('sine_cosine.png', dpi=150)
plt.show()

# *** No hold on/hold off in Python ***
# MATLAB requires  hold on  before adding a second line.
# matplotlib automatically overlays — just call ax.plot() again.

# Scatter plot
rng  = np.random.default_rng(seed=0)
x_sc = rng.standard_normal(100)
y_sc = 2 * x_sc + rng.standard_normal(100)

fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(x_sc, y_sc, s=40, alpha=0.6, color='steelblue')
# MATLAB: scatter(x,y,40,'filled','MarkerFaceAlpha',0.6)
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.set_title('Scatter Plot')
ax.grid(True)
plt.tight_layout()
plt.savefig('scatter.png', dpi=150)
plt.show()


# ============================================================
# 5.2 Subplots
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(10, 7))
# MATLAB: figure; subplot(2,2,1) ... subplot(2,2,2) ...
# Python: create all axes at once, then index into axes array

axes[0, 0].plot(x, np.sin(x),    'b-', linewidth=1.5)
axes[0, 0].set_title('sin(x)');  axes[0, 0].grid(True)

axes[0, 1].plot(x, np.cos(x),    'r-', linewidth=1.5)
axes[0, 1].set_title('cos(x)');  axes[0, 1].grid(True)

axes[1, 0].plot(x, np.sin(2*x),  'g-', linewidth=1.5)
axes[1, 0].set_title('sin(2x)'); axes[1, 0].grid(True)

axes[1, 1].plot(x, np.cos(2*x),  'm-', linewidth=1.5)
axes[1, 1].set_title('cos(2x)'); axes[1, 1].grid(True)

fig.suptitle('Trigonometric Functions', fontsize=14)    # MATLAB: sgtitle(...)
plt.tight_layout()
plt.savefig('subplots.png', dpi=150)
plt.show()

# *** axes is a 2D array when using subplots(2,2) ***
# axes[0,0] = top-left,  axes[0,1] = top-right
# axes[1,0] = bot-left,  axes[1,1] = bot-right
# For a single row: fig, axes = plt.subplots(1, 3) → axes[0], axes[1], axes[2]


# ============================================================
# 5.3 Bar, Histogram, and Box Plots
# ============================================================

# Bar chart
categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
values     = [23, 31, 28, 35, 42]

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(categories, values, color='steelblue', edgecolor='white')
ax.set_xlabel('Month'); ax.set_ylabel('Sales')
ax.set_title('Monthly Sales')
ax.grid(True, axis='y')
plt.tight_layout()
plt.savefig('bar_chart.png', dpi=150)
plt.show()

# Grouped bar chart
x_pos = np.arange(len(categories))
width = 0.35
prod_a = [23, 31, 28, 35, 42]
prod_b = [20, 28, 25, 30, 38]

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(x_pos - width/2, prod_a, width, label='Product A', color='steelblue')
ax.bar(x_pos + width/2, prod_b, width, label='Product B', color='coral')
ax.set_xticks(x_pos); ax.set_xticklabels(categories)
ax.set_xlabel('Month'); ax.set_ylabel('Sales')
ax.set_title('Monthly Sales by Product')
ax.legend(); ax.grid(True, axis='y')
plt.tight_layout()
plt.savefig('grouped_bar.png', dpi=150)
plt.show()

# Histogram
data_hist = rng.standard_normal(1000)

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(data_hist, bins=30, color='steelblue',
        edgecolor='white', alpha=0.8)
# MATLAB: histogram(data, 30)
ax.set_xlabel('Value'); ax.set_ylabel('Count')
ax.set_title('Histogram of Normal Distribution')
ax.grid(True, axis='y')
plt.tight_layout()
plt.savefig('histogram.png', dpi=150)
plt.show()

# Box plot using seaborn (much cleaner than matplotlib's boxplot)
box_data = pd.DataFrame({
    'Value': np.concatenate([
        rng.standard_normal(50),
        rng.standard_normal(50) + 1,
        rng.standard_normal(50) - 1
    ]),
    'Group': ['Group A']*50 + ['Group B']*50 + ['Group C']*50
})

fig, ax = plt.subplots(figsize=(7, 4))
sns.boxplot(data=box_data, x='Group', y='Value',
            palette='Set2', ax=ax)
# MATLAB: boxplot([g1',g2',g3'],'Labels',{'A','B','C'})
ax.set_title('Box Plot Comparison')
ax.grid(True, axis='y')
plt.tight_layout()
plt.savefig('boxplot.png', dpi=150)
plt.show()


# ============================================================
# 5.4 Heatmaps and Contour Plots
# ============================================================

x2d = np.linspace(-3, 3, 100)
y2d = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x2d, y2d)
Z    = np.exp(-(X**2 + Y**2))     # 2D Gaussian

# Heatmap (imshow)
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(Z, extent=[-3,3,-3,3], origin='lower',
               cmap='viridis', aspect='equal')
# MATLAB: imagesc(Z); colorbar
plt.colorbar(im, ax=ax)
ax.set_title('Heatmap: 2D Gaussian')
plt.tight_layout()
plt.savefig('heatmap.png', dpi=150)
plt.show()

# *** origin='lower' is important ***
# By default imshow puts row 0 at the TOP (image convention).
# origin='lower' puts row 0 at the BOTTOM (math convention).
# MATLAB's imagesc uses image convention (row 0 at top).
# Always set origin='lower' for scientific/engineering data.

# Correlation heatmap using seaborn (very common in data analysis)
df_corr = pd.DataFrame(
    rng.standard_normal((100, 4)),
    columns=['Temp', 'Pressure', 'Flow', 'Vibration']
)
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(df_corr.corr(), annot=True, fmt='.2f',
            cmap='coolwarm', center=0, ax=ax)
ax.set_title('Correlation Matrix')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=150)
plt.show()

# Filled contour plot
fig, ax = plt.subplots(figsize=(6, 5))
cp = ax.contourf(X, Y, Z, levels=20, cmap='viridis')
# MATLAB: contourf(X,Y,Z,20)
plt.colorbar(cp, ax=ax)
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.set_title('Filled Contour Plot')
plt.tight_layout()
plt.savefig('contour.png', dpi=150)
plt.show()

# 3D surface plot
from mpl_toolkits.mplot3d import Axes3D   # noqa: F401

fig  = plt.figure(figsize=(8, 6))
ax3d = fig.add_subplot(111, projection='3d')
ax3d.plot_surface(X, Y, Z, cmap='viridis', linewidth=0, antialiased=True)
# MATLAB: surf(X,Y,Z); shading interp
ax3d.set_xlabel('x'); ax3d.set_ylabel('y'); ax3d.set_zlabel('z')
ax3d.set_title('3D Surface Plot')
plt.tight_layout()
plt.savefig('surface_3d.png', dpi=150)
plt.show()


# ============================================================
# 5.5 Customizing Appearance
# ============================================================

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(x, np.sin(x),
        color=(0.2, 0.4, 0.8),     # MATLAB: 'Color',[0.2,0.4,0.8]
        linewidth=2.5,              # MATLAB: 'LineWidth',2.5
        linestyle='-',              # MATLAB: 'LineStyle','-'
        marker='o',                 # MATLAB: 'Marker','o'
        markersize=5,               # MATLAB: 'MarkerSize',4
        markevery=10)               # MATLAB: 'MarkerIndices',1:10:end

# Axis limits
ax.set_xlim([0, 2*np.pi])          # MATLAB: xlim([0, 2*pi])
ax.set_ylim([-1.2, 1.2])           # MATLAB: ylim([-1.2, 1.2])

# Custom ticks
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'], fontsize=11)
# MATLAB: xticks([...]); xticklabels({...})

ax.set_xlabel('Angle (rad)', fontsize=13)   # MATLAB: xlabel(...,'FontSize',13)
ax.set_ylabel('Amplitude',   fontsize=13)
ax.set_title('Customized Sine Wave',        fontsize=14)
ax.tick_params(labelsize=11)                # MATLAB: set(gca,'FontSize',12)
ax.grid(True)

plt.tight_layout()
plt.savefig('customized.png', dpi=150)
plt.show()

# Quick styling with seaborn themes
# Add this at the top of your script for publication-quality defaults:
#   sns.set_theme(style='whitegrid', palette='deep', font_scale=1.2)
# Options: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'
# This one line replaces dozens of set(gca,...) calls in MATLAB.


# ============================================================
# 5.6 Saving Figures
# ============================================================

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x, np.sin(x), 'b-', linewidth=2)
ax.set_title('Saved Figure'); ax.grid(True)
plt.tight_layout()

# PNG — for reports, presentations, web
plt.savefig('sine_wave.png', dpi=300, bbox_inches='tight')
# MATLAB: saveas(fig,'sine_wave.png')

# PDF — vector format, best for publications
plt.savefig('sine_wave.pdf', bbox_inches='tight')
# MATLAB: exportgraphics(fig,'sine_wave.pdf','ContentType','vector')

# SVG — vector, editable in Illustrator / Inkscape
plt.savefig('sine_wave.svg', bbox_inches='tight')

# *** Always use bbox_inches='tight' ***
# Without it, axis labels and titles are often clipped in the saved file.
# MATLAB handles this automatically — Python does not.

plt.show()


# ============================================================
# 5.7 Engineering Plot: Signal Analysis
# ============================================================
# Time domain + frequency domain — the most common plot pair
# in experimental and simulation work.

Fs   = 1000                                 # sampling frequency (Hz)
t_s  = np.arange(0, 1, 1/Fs)               # MATLAB: 0:1/Fs:1-1/Fs
f1   = 50;  f2 = 120                        # signal frequencies
sig  = (np.sin(2*np.pi*f1*t_s)
      + 0.5*np.sin(2*np.pi*f2*t_s)
      + 0.2*rng.standard_normal(len(t_s)))

# FFT
N    = len(sig)
Y    = np.fft.fft(sig)                      # MATLAB: fft(sig)
P2   = np.abs(Y / N)
P1   = P2[:N//2 + 1]
P1[1:-1] *= 2
f_ax = Fs * np.arange(N//2 + 1) / N        # frequency axis

fig, axes = plt.subplots(2, 1, figsize=(10, 6))

axes[0].plot(t_s[:200], sig[:200], 'b-', linewidth=1)
axes[0].set_xlabel('Time (s)'); axes[0].set_ylabel('Amplitude')
axes[0].set_title('Time Domain Signal'); axes[0].grid(True)

axes[1].plot(f_ax, P1, 'r-', linewidth=1.5)
axes[1].set_xlabel('Frequency (Hz)'); axes[1].set_ylabel('|Amplitude|')
axes[1].set_title('Frequency Spectrum (FFT)')
axes[1].set_xlim([0, 200]); axes[1].grid(True)

plt.tight_layout()
plt.savefig('signal_fft.png', dpi=150, bbox_inches='tight')
plt.show()


# ============================================================
# Chapter 5 Summary: Key Differences to Remember
# ============================================================
#
# 1. TWO INTERFACES — use OOP style for real work:
#    fig, ax = plt.subplots()  then  ax.plot(), ax.set_title()
#    pyplot style (plt.plot) is fine for quick checks only.
#
# 2. NO hold on/hold off — just call ax.plot() multiple times.
#
# 3. SUBPLOTS return a 2D array: axes[row, col]
#    MATLAB: subplot(2,2,1) uses a single index.
#
# 4. imshow needs origin='lower' for scientific data.
#    Default puts row 0 at the top (image convention).
#
# 5. ALWAYS use bbox_inches='tight' when saving:
#    plt.savefig('file.png', dpi=300, bbox_inches='tight')
#
# 6. seaborn one-liner for publication style:
#    sns.set_theme(style='whitegrid', font_scale=1.2)
