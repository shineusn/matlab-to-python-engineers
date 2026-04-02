# ============================================================
# Chapter 8: Modern Engineering Workflows and Migration Tips
# "From MATLAB to Python for Engineers and Scientists"
# Python Reference Code
# ============================================================


# ============================================================
# 8.1 Project Structure — From MATLAB Scripts to Python Modules
# ============================================================
#
# MATLAB workflow:
#   script1.m, script2.m, helper.m — all in one folder
#   run each script manually, share variables via workspace
#
# Python equivalent (recommended structure):
#
#   my_project/
#   ├── main.py              ← entry point
#   ├── requirements.txt     ← dependencies
#   ├── README.md
#   ├── src/
#   │   ├── __init__.py
#   │   ├── signal_utils.py  ← reusable functions
#   │   ├── data_io.py
#   │   └── plotting.py
#   ├── data/
#   │   └── measurements.csv
#   ├── results/
#   │   └── figures/
#   └── tests/
#       └── test_signal_utils.py
#
# Key difference: Python uses MODULES (importable .py files)
# instead of MATLAB's collection of .m files.
# Functions in one file can be imported and reused cleanly.


# ============================================================
# 8.2 Writing Reusable Modules (replacing .m function files)
# ============================================================

# --- File: src/signal_utils.py ---
# (shown here inline for the book — in practice this is a separate file)

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from pathlib import Path


def bandpass_filter(x, fs, f_low, f_high, order=4):
    """
    Apply a zero-phase Butterworth bandpass filter.

    Parameters
    ----------
    x      : array-like  — input signal
    fs     : float       — sampling frequency (Hz)
    f_low  : float       — lower cutoff frequency (Hz)
    f_high : float       — upper cutoff frequency (Hz)
    order  : int         — filter order (default 4)

    Returns
    -------
    x_filt : ndarray     — filtered signal

    Example
    -------
    >>> x_filt = bandpass_filter(x, fs=1000, f_low=10, f_high=200)
    """
    nyq  = fs / 2
    b, a = signal.butter(order, [f_low/nyq, f_high/nyq], btype='bandpass')
    return signal.filtfilt(b, a, x)


def compute_spectrum(x, fs):
    """
    Compute the single-sided amplitude spectrum of a signal.

    Parameters
    ----------
    x  : array-like — input signal
    fs : float      — sampling frequency (Hz)

    Returns
    -------
    f  : ndarray — frequency axis (Hz)
    P  : ndarray — amplitude spectrum
    """
    N  = len(x)
    Y  = np.fft.fft(x)
    P  = 2 * np.abs(Y[:N//2 + 1]) / N
    P[0]  /= 2
    f  = fs * np.arange(N//2 + 1) / N
    return f, P


def plot_time_freq(t, x, fs, title='Signal Analysis',
                   xlim_freq=None, save_path=None):
    """
    Plot time domain and frequency spectrum side by side.

    Parameters
    ----------
    t          : ndarray — time vector (s)
    x          : ndarray — signal values
    fs         : float   — sampling frequency (Hz)
    title      : str     — figure title
    xlim_freq  : tuple   — frequency axis limits e.g. (0, 500)
    save_path  : str     — if provided, save figure to this path
    """
    f, P = compute_spectrum(x, fs)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(t, x, linewidth=0.8)
    axes[0].set_xlabel('Time (s)');  axes[0].set_ylabel('Amplitude')
    axes[0].set_title('Time Domain'); axes[0].grid(True)

    axes[1].plot(f, P, 'r-', linewidth=1.2)
    axes[1].set_xlabel('Frequency (Hz)'); axes[1].set_ylabel('|Amplitude|')
    axes[1].set_title('Frequency Spectrum'); axes[1].grid(True)
    if xlim_freq:
        axes[1].set_xlim(xlim_freq)

    fig.suptitle(title, fontsize=13)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Figure saved: {save_path}")
    plt.show()

# Usage (from main.py or a notebook):
# from src.signal_utils import bandpass_filter, plot_time_freq
#
# x_filt = bandpass_filter(x_raw, fs=5000, f_low=5, f_high=500)
# plot_time_freq(t, x_filt, fs=5000, title='Filtered Vibration',
#                xlim_freq=(0, 300), save_path='results/vibration.png')

# *** Advantages over MATLAB function files ***
# 1. All related functions in ONE file (not scattered .m files)
# 2. Docstrings are readable in IDE — hover to see docs
# 3. Import only what you need: from signal_utils import bandpass_filter
# 4. Easy to test, share, and version control


# ============================================================
# 8.3 Virtual Environments — Replacing MATLAB's Fixed Toolboxes
# ============================================================
#
# MATLAB: toolboxes are installed globally, version conflicts are rare
#         but licenses are expensive and tied to the installation.
#
# Python: packages are installed per-project using virtual environments.
#         Free, flexible, but requires a little setup.
#
# WORKFLOW (run in terminal, not Python):
#
#   # Create a virtual environment
#   python -m venv venv
#
#   # Activate it
#   source venv/bin/activate        # macOS / Linux
#   venv\Scripts\activate           # Windows
#
#   # Install packages
#   pip install numpy scipy pandas matplotlib seaborn opencv-python scikit-image
#
#   # Save exact versions for reproducibility (like MATLAB's version pinning)
#   pip freeze > requirements.txt
#
#   # Someone else can recreate your exact environment:
#   pip install -r requirements.txt
#
#   # Deactivate when done
#   deactivate
#
# Using conda (recommended if you came from MATLAB — similar to
# MATLAB's environment concept):
#
#   conda create -n myproject python=3.11
#   conda activate myproject
#   conda install numpy scipy pandas matplotlib scikit-image
#   conda env export > environment.yml
#   conda env create -f environment.yml   # recreate on another machine


# ============================================================
# 8.4 Version Control with Git — Replacing MATLAB's "save as v2"
# ============================================================
#
# MATLAB habit: save files as script_v1.m, script_final.m,
#               script_final2.m, script_FINAL_USE_THIS.m ...
#
# Python (and modern engineering) habit: use Git.
#
# ESSENTIAL GIT COMMANDS (run in terminal):
#
#   git init                          # start tracking a project
#   git add .                         # stage all changes
#   git commit -m "Add bandpass filter function"  # save a snapshot
#   git log --oneline                 # see history
#   git diff                          # see what changed
#
#   # Connect to GitHub
#   git remote add origin https://github.com/username/repo.git
#   git push -u origin main
#
#   # Create a branch for experimenting (safe — doesn't touch main)
#   git checkout -b experiment/new-filter
#   # ... make changes ...
#   git checkout main                 # switch back safely
#
# Recommended .gitignore for Python engineering projects:
# (already included in your companion repository)

gitignore_content = """
__pycache__/
*.py[cod]
*.ipynb_checkpoints/
.env
venv/
.DS_Store
*.mat
data/raw/
results/figures/*.png
"""
# Save this as .gitignore in your project root.


# ============================================================
# 8.5 Migrating MATLAB Scripts to Python — Practical Checklist
# ============================================================

migration_checklist = {
    "Indexing": [
        "Replace all v(i) with v[i-1]  — shift every index by 1",
        "Replace A(i,j) with A[i-1, j-1]",
        "Replace v(end) with v[-1]",
        "Replace v(1:n) with v[0:n]  — Python end is exclusive",
        "Replace v(1:2:end) with v[::2]",
    ],
    "Operators": [
        "Replace A * B (matrix mul) with A @ B",
        "Replace A .* B (element mul) with A * B",
        "Replace A ./ B with A / B",
        "Replace A .^ n with A ** n",
        "Replace A' (transpose) with A.T",
        "Replace A \\ b (linear solve) with np.linalg.solve(A, b)",
    ],
    "Control flow": [
        "Remove all 'end' keywords — use indentation instead",
        "Replace elseif with elif",
        "Replace for i = 1:n with for i in range(1, n+1):",
        "Replace % comments with # comments",
    ],
    "Functions": [
        "Move function definitions to the top of file or a separate module",
        "Replace function [out1, out2] = f(x) with def f(x): return out1, out2",
        "Replace nargin checks with default argument values: def f(x, n=10):",
    ],
    "I/O": [
        "Replace load('file.mat') with scipy.io.loadmat('file.mat')",
        "Replace save('file.mat','var') with np.save or scipy.io.savemat",
        "Replace readtable('f.csv') with pd.read_csv('f.csv')",
        "Replace imshow(img) with ax.imshow(img); plt.show()",
    ],
    "Signal Processing": [
        "Replace fft(x) with np.fft.fft(x)",
        "Replace [b,a]=butter(n,Wn) with signal.butter(n,Wn)",
        "Replace filtfilt(b,a,x) with signal.filtfilt(b,a,x)  — same!",
        "Replace [pxx,f]=pwelch(x,[],[],[],Fs) with f,pxx=signal.welch(x,fs=Fs)",
        "NOTE: pwelch and welch return in OPPOSITE order",
    ],
    "Image Processing": [
        "Replace imread with skimage.io.imread or cv2.imread",
        "If using cv2: convert BGR→RGB with cv2.cvtColor(img, cv2.COLOR_BGR2RGB)",
        "Replace rgb2gray with skimage.color.rgb2gray (returns float, not uint8)",
        "Replace imgaussfilt(img,s) with skimage.filters.gaussian(img, sigma=s)",
        "Replace imshow(img) with ax.imshow(img, cmap='gray'); plt.show()",
    ],
}

print("=== MATLAB to Python Migration Checklist ===\n")
for category, items in migration_checklist.items():
    print(f"[ {category} ]")
    for item in items:
        print(f"  ✓ {item}")
    print()


# ============================================================
# 8.6 Using AI Tools to Speed Up Migration
# ============================================================
#
# AI coding assistants (Claude, GitHub Copilot, etc.) can
# dramatically speed up MATLAB-to-Python migration.
# Here is how to use them effectively:
#
# PROMPT TEMPLATE 1 — Convert a MATLAB function:
# ------------------------------------------------
# "Convert this MATLAB function to Python using NumPy and SciPy.
#  Keep the same logic and add comments explaining any differences
#  in indexing or function names.
#
#  MATLAB code:
#  [your MATLAB code here]"
#
# PROMPT TEMPLATE 2 — Debug a conversion issue:
# ------------------------------------------------
# "I converted this MATLAB code to Python but the results differ.
#  MATLAB code: [...]
#  Python code: [...]
#  MATLAB output: [...]
#  Python output: [...]
#  What is wrong?"
#
# PROMPT TEMPLATE 3 — Find the Python equivalent:
# ------------------------------------------------
# "What is the Python/NumPy/SciPy equivalent of MATLAB's
#  [function name]? Show a side-by-side example."
#
# IMPORTANT — always verify AI output:
# • Run the code and check numerical results match MATLAB
# • Pay special attention to indexing (0 vs 1 based)
# • Check matrix multiply operators (* vs @)
# • Verify array shapes with print(array.shape)


# ============================================================
# 8.7 Packaging and Sharing Your Work
# ============================================================

# --- Sharing a script (simplest) ---
# Send the .py file + requirements.txt
# Recipient runs: pip install -r requirements.txt && python script.py

# --- Sharing a Jupyter notebook ---
# .ipynb files contain code + outputs + markdown explanations
# Open with: jupyter lab  or  jupyter notebook
# Export to HTML/PDF for reports: File → Export

# --- Creating a simple command-line tool ---
# Add this to your script to accept arguments from the terminal:

import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Vibration analysis tool'
    )
    parser.add_argument('--input',  type=str, required=True,
                        help='Path to input CSV file')
    parser.add_argument('--fs',     type=float, default=1000,
                        help='Sampling frequency in Hz (default: 1000)')
    parser.add_argument('--output', type=str, default='results/',
                        help='Output directory for figures')
    return parser.parse_args()

# Usage from terminal:
# python analyze.py --input data/vibration.csv --fs 5000 --output results/

# This replaces the MATLAB habit of hardcoding file paths inside scripts.
# Your colleagues can run the tool without opening the code.


# ============================================================
# 8.8 Complete Migration Example: MATLAB Script → Python Module
# ============================================================
# Side-by-side comparison of the same analysis in both languages.

# MATLAB version (what you used to write):
matlab_code = """
% analyze_vibration.m
function analyze_vibration(filename, Fs)
    % Load data
    data = readmatrix(filename);
    t    = data(:,1)';
    x    = data(:,2)';

    % Band-pass filter 5-500 Hz
    [b,a]  = butter(4, [5,500]/(Fs/2), 'bandpass');
    x_filt = filtfilt(b, a, x);

    % FFT
    N  = length(x_filt);
    Y  = fft(x_filt);
    P2 = abs(Y/N);
    P1 = P2(1:N/2+1);
    P1(2:end-1) = 2*P1(2:end-1);
    f  = Fs*(0:(N/2))/N;

    % Plot
    figure;
    subplot(2,1,1)
    plot(t, x_filt)
    xlabel('Time (s)'); ylabel('Amplitude')
    title('Filtered Signal'); grid on

    subplot(2,1,2)
    plot(f, P1, 'r-')
    xlabel('Frequency (Hz)'); ylabel('|Amplitude|')
    title('FFT Spectrum'); xlim([0,500]); grid on

    saveas(gcf, 'vibration_analysis.png')
end
"""

# Python equivalent (what you write now):
def analyze_vibration(filename, fs=1000, output_dir='results/'):
    """
    Load vibration data, filter, compute FFT, and save figure.

    Parameters
    ----------
    filename   : str   — path to CSV file (columns: time, signal)
    fs         : float — sampling frequency (Hz)
    output_dir : str   — directory to save output figures
    """
    import pandas as pd

    # Load data
    df     = pd.read_csv(filename, header=None, names=['time', 'signal'])
    t      = df['time'].values
    x      = df['signal'].values

    # Band-pass filter 5–500 Hz
    x_filt = bandpass_filter(x, fs=fs, f_low=5, f_high=500)

    # FFT
    f_ax, P = compute_spectrum(x_filt, fs)

    # Save figure
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    save_path = Path(output_dir) / 'vibration_analysis.png'

    plot_time_freq(t, x_filt, fs,
                   title='Vibration Analysis',
                   xlim_freq=(0, 500),
                   save_path=str(save_path))

    return f_ax, P


# ============================================================
# 8.9 Where to Go Next
# ============================================================

next_steps = {
    "Deepen NumPy / SciPy": [
        "NumPy documentation: numpy.org/doc",
        "SciPy documentation: docs.scipy.org",
        "Book: 'Python for Data Analysis' — Wes McKinney (pandas creator)",
    ],
    "Scientific Python ecosystem": [
        "SymPy   — symbolic math (like MATLAB Symbolic Toolbox)",
        "FEniCS  — finite element analysis",
        "PyVista — 3D visualization (like MATLAB's 3D plots but better)",
        "Numba   — JIT compilation for speed (approach MATLAB MEX speed)",
    ],
    "Machine Learning and AI": [
        "scikit-learn  — classical ML (clustering, regression, classification)",
        "PyTorch       — deep learning",
        "Hugging Face  — pre-trained models and datasets",
    ],
    "Engineering-specific": [
        "control   — control systems (replaces Control Systems Toolbox)",
        "pyFEM     — finite element methods",
        "OpenMDAO  — multidisciplinary design optimization",
        "Pint      — unit-aware calculations (avoids unit mistakes)",
    ],
    "Stay current": [
        "Follow Scientific Python ecosystem: scientific-python.org",
        "SciPy conference talks on YouTube",
        "Real Python tutorials: realpython.com",
    ],
}

print("\n=== Where to Go Next ===\n")
for topic, resources in next_steps.items():
    print(f"[ {topic} ]")
    for r in resources:
        print(f"  → {r}")
    print()


# ============================================================
# Chapter 8 Summary: The Modern Python Engineering Workflow
# ============================================================
#
# MATLAB workflow:              Python equivalent:
# ─────────────────────────    ──────────────────────────────
# .m script files          →   .py modules with functions
# workspace variables      →   function arguments / return values
# MATLAB path              →   import + virtual environment
# version: script_v3.m    →   git commit + branches
# toolbox license          →   pip install (free, open source)
# MATLAB editor            →   VS Code + Python extension
#                              or JupyterLab
# saveas(fig,'file.png')   →   plt.savefig('file.png', dpi=300,
#                                           bbox_inches='tight')
# disp / fprintf           →   print() / f-strings
# try / catch              →   try / except
#
# The transition takes time — be patient with yourself.
# After a few months of consistent use, Python workflows feel
# natural, and the open ecosystem opens doors that MATLAB cannot.
