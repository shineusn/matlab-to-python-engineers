# ============================================================
# Chapter 7: Signal Processing
# "From MATLAB to Python for Engineers and Scientists"
# Python Reference Code
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from scipy.fft import fft, fftfreq


# ============================================================
# 7.1 Generating Test Signals
# ============================================================

Fs  = 1000                          # sampling frequency (Hz)
T   = 1 / Fs                        # sampling period
t   = np.arange(0, 1, T)           # time vector  — MATLAB: 0:T:1-T
N   = len(t)                        # number of samples

# Pure sine wave
f1  = 50
x1  = np.sin(2 * np.pi * f1 * t)   # MATLAB: sin(2*pi*f1*t)

# Composite signal (two tones + noise)
rng = np.random.default_rng(seed=0)
f2  = 120
x   = (np.sin(2 * np.pi * f1 * t)
     + 0.5 * np.sin(2 * np.pi * f2 * t)
     + 0.2 * rng.standard_normal(N))

# Chirp signal (frequency sweep: 10 → 200 Hz over 1 second)
x_chirp = signal.chirp(t, f0=10, f1=200, t1=1, method='linear')
# MATLAB: chirp(t, 10, 1, 200)

# Square wave
x_sq = signal.square(2 * np.pi * 10 * t)   # MATLAB: square(2*pi*10*t)

# Plot
fig, axes = plt.subplots(2, 1, figsize=(10, 6))
axes[0].plot(t[:200], x[:200])
axes[0].set_xlabel('Time (s)'); axes[0].set_ylabel('Amplitude')
axes[0].set_title('Composite Signal (first 0.2 s)'); axes[0].grid(True)

axes[1].plot(t, x_chirp)
axes[1].set_xlabel('Time (s)'); axes[1].set_ylabel('Amplitude')
axes[1].set_title('Chirp Signal'); axes[1].grid(True)
plt.tight_layout(); plt.savefig('ch7_signals.png', dpi=150); plt.show()


# ============================================================
# 7.2 Fourier Transform and Frequency Analysis
# ============================================================

# FFT — same algorithm as MATLAB fft()
Y    = fft(x)                           # MATLAB: fft(x)
P2   = np.abs(Y / N)
P1   = P2[:N // 2 + 1]
P1[1:-1] *= 2                           # double amplitudes (single-sided)
f_ax = Fs * np.arange(N // 2 + 1) / N  # frequency axis  — MATLAB: Fs*(0:(N/2))/N

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(f_ax, P1, 'r-', linewidth=1.5)
ax.set_xlabel('Frequency (Hz)'); ax.set_ylabel('|Amplitude|')
ax.set_title('Single-Sided Amplitude Spectrum')
ax.set_xlim([0, 300]); ax.grid(True)
plt.tight_layout(); plt.savefig('ch7_fft.png', dpi=150); plt.show()

# *** fftfreq — cleaner way to build the frequency axis ***
freqs    = fftfreq(N, d=1/Fs)          # returns both positive and negative freqs
pos_mask = freqs >= 0                   # keep only positive side
# This avoids manual calculation of the frequency axis above.

# Power Spectral Density — Welch method (better for noisy signals)
f_psd, pxx = signal.welch(x, fs=Fs, nperseg=256)   # MATLAB: pwelch(x,[],[],[],Fs)

fig, ax = plt.subplots(figsize=(9, 4))
ax.semilogy(f_psd, pxx)                # MATLAB: semilogy(f_psd, pxx)
ax.set_xlabel('Frequency (Hz)'); ax.set_ylabel('PSD (V²/Hz)')
ax.set_title('Power Spectral Density (Welch)'); ax.grid(True)
plt.tight_layout(); plt.savefig('ch7_psd.png', dpi=150); plt.show()

# *** welch argument order differs from MATLAB ***
# MATLAB: [pxx, f] = pwelch(x, window, noverlap, nfft, Fs)
# Python:  f, pxx  = signal.welch(x, fs=Fs, nperseg=...)
# Note the return order is REVERSED: Python returns (f, pxx), MATLAB returns (pxx, f)

# Spectrogram (Short-Time Fourier Transform)
f_sg, t_sg, Sxx = signal.spectrogram(x_chirp, fs=Fs,
                                      nperseg=128, noverlap=120)
# MATLAB: spectrogram(x_chirp, 128, 120, 256, Fs)

fig, ax = plt.subplots(figsize=(9, 4))
ax.pcolormesh(t_sg, f_sg, 10 * np.log10(Sxx + 1e-12),
              shading='gouraud', cmap='viridis')
ax.set_xlabel('Time (s)'); ax.set_ylabel('Frequency (Hz)')
ax.set_title('Spectrogram of Chirp Signal')
plt.colorbar(ax.collections[0], ax=ax, label='Power (dB)')
plt.tight_layout(); plt.savefig('ch7_spectrogram.png', dpi=150); plt.show()


# ============================================================
# 7.3 Digital Filters — Design and Application
# ============================================================

Fs  = 1000

# Low-pass Butterworth filter (cutoff 80 Hz, order 4)
b_lp, a_lp = signal.butter(4, 80 / (Fs/2), btype='low')
# MATLAB: [b,a] = butter(4, 80/(Fs/2), 'low')
# Note: Python uses btype=, MATLAB uses a string argument

# High-pass Butterworth filter (cutoff 30 Hz)
b_hp, a_hp = signal.butter(4, 30 / (Fs/2), btype='high')

# Band-pass filter (30–80 Hz)
b_bp, a_bp = signal.butter(4, [30/(Fs/2), 80/(Fs/2)], btype='bandpass')
# MATLAB: butter(4, [30,80]/(Fs/2), 'bandpass')

# Band-stop / notch filter (45–55 Hz)
b_bs, a_bs = signal.butter(4, [45/(Fs/2), 55/(Fs/2)], btype='bandstop')

# Frequency response
w, h = signal.freqz(b_lp, a_lp, worN=1024, fs=Fs)  # MATLAB: freqz(b,a,1024,Fs)

fig, axes = plt.subplots(2, 1, figsize=(9, 6))
axes[0].plot(w, 20 * np.log10(np.abs(h)))
axes[0].set_ylabel('Magnitude (dB)'); axes[0].set_title('Low-Pass Filter Response')
axes[0].set_xlim([0, Fs/2]); axes[0].grid(True); axes[0].axvline(80, color='r', ls='--')

axes[1].plot(w, np.angle(h) * 180 / np.pi)
axes[1].set_xlabel('Frequency (Hz)'); axes[1].set_ylabel('Phase (degrees)')
axes[1].set_xlim([0, Fs/2]); axes[1].grid(True)
plt.tight_layout(); plt.savefig('ch7_filter_response.png', dpi=150); plt.show()

# Apply filter — zero-phase (filtfilt)
t   = np.arange(0, 1, 1/Fs)
x_f = (np.sin(2*np.pi*50*t)
     + np.sin(2*np.pi*200*t)
     + 0.2*rng.standard_normal(len(t)))

x_filt_lp = signal.filtfilt(b_lp, a_lp, x_f)  # MATLAB: filtfilt(b,a,x)
x_filt_hp = signal.filtfilt(b_hp, a_hp, x_f)

# *** filtfilt vs lfilter ***
# signal.filtfilt — zero-phase (applies filter forward then backward)
#                   matches MATLAB's filtfilt exactly
#                   no phase distortion — use this for analysis
# signal.lfilter  — causal filter (forward pass only)
#                   introduces phase delay
#                   matches MATLAB's filter() function

fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
for ax, sig_data, title in zip(axes,
    [x_f[:200], x_filt_lp[:200], x_filt_hp[:200]],
    ['Original', 'Low-pass filtered', 'High-pass filtered']):
    ax.plot(t[:200], sig_data)
    ax.set_title(title); ax.grid(True); ax.set_ylabel('Amplitude')
axes[-1].set_xlabel('Time (s)')
plt.tight_layout(); plt.savefig('ch7_filtered.png', dpi=150); plt.show()


# ============================================================
# 7.4 FIR Filters
# ============================================================

Fs    = 1000
order = 64
fc    = 80      # cutoff frequency (Hz)

# FIR filter using window method (Hamming window by default)
b_fir = signal.firwin(order + 1, fc / (Fs/2), window='hamming')
# MATLAB: fir1(order, fc/(Fs/2), 'low')  — hamming is also default

# Apply FIR filter
t   = np.arange(0, 1, 1/Fs)
x_f = (np.sin(2*np.pi*50*t)
     + np.sin(2*np.pi*200*t)
     + 0.2*rng.standard_normal(len(t)))

x_fir = signal.filtfilt(b_fir, 1.0, x_f)  # MATLAB: filtfilt(b_fir, 1, x)

# Frequency response
w_fir, h_fir = signal.freqz(b_fir, 1.0, worN=1024, fs=Fs)

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(w_fir, 20 * np.log10(np.abs(h_fir) + 1e-12))
ax.set_xlabel('Frequency (Hz)'); ax.set_ylabel('Magnitude (dB)')
ax.set_title('FIR Low-Pass Filter Response')
ax.axvline(fc, color='r', ls='--', label=f'Cutoff {fc} Hz')
ax.set_xlim([0, Fs/2]); ax.legend(); ax.grid(True)
plt.tight_layout(); plt.savefig('ch7_fir.png', dpi=150); plt.show()

# *** IIR vs FIR — same trade-offs as in MATLAB ***
# IIR (Butterworth, Chebyshev): lower order, computationally efficient
#                                has phase distortion (use filtfilt to fix)
# FIR (firwin): linear phase, stable, higher order needed
#               better for applications where phase matters


# ============================================================
# 7.5 Correlation and Convolution
# ============================================================

Fs  = 1000
t   = np.arange(0, 1, 1/Fs)
x_c = np.sin(2*np.pi*5*t) + 0.5*rng.standard_normal(len(t))
y_c = np.roll(x_c, 50) + 0.3*rng.standard_normal(len(t))  # MATLAB: circshift(x,50)

# Cross-correlation
correlation = signal.correlate(x_c, y_c, mode='full')         # MATLAB: xcorr(x,y)
lags        = signal.correlation_lags(len(x_c), len(y_c), mode='full')
correlation /= np.max(np.abs(correlation))                     # normalize

delay_samples = lags[np.argmax(correlation)]
delay_ms      = delay_samples / Fs * 1000
print(f"Detected delay: {delay_ms:.1f} ms")

# *** xcorr vs correlate argument order ***
# MATLAB: xcorr(x, y) — cross-correlation of x WITH y
# Python: signal.correlate(x, y) — same convention
# But MATLAB xcorr returns [r, lags] in one call;
# Python needs signal.correlation_lags() separately.

# Auto-correlation
autocorr = signal.correlate(x_c, x_c, mode='full')
lags_auto = signal.correlation_lags(len(x_c), len(x_c), mode='full')
autocorr /= np.max(np.abs(autocorr))

# Convolution
h   = np.ones(20) / 20                  # moving average kernel
y_conv = signal.convolve(x_c, h, mode='same')  # MATLAB: conv(x,h,'same')

fig, axes = plt.subplots(2, 1, figsize=(10, 6))
axes[0].plot(lags / Fs * 1000, correlation)
axes[0].set_xlabel('Lag (ms)'); axes[0].set_ylabel('Correlation')
axes[0].set_title('Cross-Correlation'); axes[0].grid(True)
axes[0].axvline(delay_ms, color='r', ls='--', label=f'Peak at {delay_ms:.0f} ms')
axes[0].legend()

axes[1].plot(t[:200], x_c[:200], alpha=0.6, label='Original')
axes[1].plot(t[:200], y_conv[:200], linewidth=2, label='Smoothed (conv)')
axes[1].set_xlabel('Time (s)'); axes[1].set_ylabel('Amplitude')
axes[1].set_title('Convolution (Moving Average)'); axes[1].legend(); axes[1].grid(True)
plt.tight_layout(); plt.savefig('ch7_correlation.png', dpi=150); plt.show()


# ============================================================
# 7.6 Resampling
# ============================================================

Fs_orig = 1000
t_orig  = np.arange(0, 1, 1/Fs_orig)
x_orig  = np.sin(2*np.pi*50*t_orig) + 0.1*rng.standard_normal(len(t_orig))

# Downsample by factor of 4 (1000 Hz → 250 Hz) with anti-aliasing
x_down = signal.decimate(x_orig, q=4)              # MATLAB: downsample(x,4) + anti-alias

# Resample to arbitrary rate (500 Hz)
num_samples = int(len(x_orig) * 500 / Fs_orig)
x_re = signal.resample(x_orig, num_samples)        # MATLAB: resample(x,500,Fs_orig)

# *** signal.decimate vs signal.resample ***
# decimate: integer downsampling ratio, includes anti-aliasing filter
#           matches MATLAB resample() for downsampling
# resample: arbitrary ratio, uses FFT-based method
#           use when target rate is not an integer factor of original

# Upsample with interpolation
x_up = signal.resample(x_orig, len(x_orig) * 2)   # MATLAB: upsample(x,2)

print(f"Original samples : {len(x_orig)}")
print(f"Downsampled      : {len(x_down)}")
print(f"Resampled 500 Hz : {len(x_re)}")
print(f"Upsampled        : {len(x_up)}")


# ============================================================
# 7.7 Real Engineering Case: Vibration Analysis
# ============================================================
# Rotating machinery fault detection — a classic signal processing
# application in mechanical and industrial engineering.
#
# Goal: detect bearing fault frequency hidden in broadband noise.

Fs    = 5000                        # 5 kHz sampling
t     = np.arange(0, 2, 1/Fs)      # 2 seconds
N     = len(t)

f_rot   = 25.0                      # shaft rotation: 25 Hz = 1500 RPM
f_fault = f_rot * 3.5               # bearing fault frequency (BPFO example)

# Simulate vibration signal
x_vib = (1.0 * np.sin(2*np.pi*f_rot*t)         # fundamental
        + 0.4 * np.sin(2*np.pi*2*f_rot*t)       # 2nd harmonic
        + 0.2 * np.sin(2*np.pi*f_fault*t)        # fault frequency
        + 0.5 * rng.standard_normal(N))           # broadband noise

# Step 1: Band-pass filter (5–500 Hz)
b, a    = signal.butter(4, [5/(Fs/2), 500/(Fs/2)], btype='bandpass')
x_filt  = signal.filtfilt(b, a, x_vib)

# Step 2: FFT of filtered signal
Y    = fft(x_filt)
P2   = np.abs(Y / N)
P1   = P2[:N//2 + 1]
P1[1:-1] *= 2
f_ax = Fs * np.arange(N//2 + 1) / N

# Step 3: Welch PSD for better frequency resolution
f_psd, pxx = signal.welch(x_filt, fs=Fs, nperseg=2048, noverlap=1024, nfft=4096)

# Step 4: Find peaks in spectrum
peaks, props = signal.find_peaks(P1, height=0.02, distance=20)
peak_freqs   = f_ax[peaks]
peak_amps    = P1[peaks]

print("Detected spectral peaks:")
for pf, pa in zip(peak_freqs[peak_freqs < 300], peak_amps[peak_freqs < 300]):
    print(f"  {pf:.1f} Hz  (amplitude {pa:.4f})")

# Step 5: Full results plot
fig, axes = plt.subplots(3, 1, figsize=(12, 9))

# Time domain
axes[0].plot(t[:1000], x_vib[:1000], alpha=0.6, linewidth=0.8)
axes[0].set_xlabel('Time (s)'); axes[0].set_ylabel('Acceleration (g)')
axes[0].set_title('Raw Vibration Signal'); axes[0].grid(True)

# FFT spectrum
axes[1].plot(f_ax, P1, 'b-', linewidth=1)
axes[1].set_xlabel('Frequency (Hz)'); axes[1].set_ylabel('|Amplitude|')
axes[1].set_title('FFT Spectrum')
axes[1].set_xlim([0, 300]); axes[1].grid(True)

# Mark key frequencies
for freq, label, color in [
    (f_rot,     '1× rot',  'r'),
    (2*f_rot,   '2× rot',  'g'),
    (f_fault,   'Fault',   'm'),
]:
    axes[1].axvline(freq, color=color, ls='--', linewidth=1.5, label=label)
axes[1].legend(loc='upper right')

# Welch PSD
axes[2].semilogy(f_psd, pxx, 'k-', linewidth=1)
axes[2].set_xlabel('Frequency (Hz)'); axes[2].set_ylabel('PSD (g²/Hz)')
axes[2].set_title('Welch PSD — better resolution for noisy signals')
axes[2].set_xlim([0, 300]); axes[2].grid(True)
for freq, color in [(f_rot,'r'), (2*f_rot,'g'), (f_fault,'m')]:
    axes[2].axvline(freq, color=color, ls='--', linewidth=1.2)

fig.suptitle('Vibration Analysis: Rotating Machinery Fault Detection',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('ch7_vibration_analysis.png', dpi=150, bbox_inches='tight')
plt.show()


# ============================================================
# Chapter 7 Summary: Key Differences to Remember
# ============================================================
#
# 1. scipy.signal replaces MATLAB's Signal Processing Toolbox.
#    Function names are similar but not identical.
#
# 2. welch returns (f, pxx) — OPPOSITE order to MATLAB's (pxx, f):
#    MATLAB: [pxx, f] = pwelch(x, ...)
#    Python:  f, pxx  = signal.welch(x, ...)
#
# 3. butter normalization — divide cutoff by Fs/2 (same as MATLAB):
#    signal.butter(4, fc / (Fs/2), btype='low')
#
# 4. Use filtfilt for zero-phase filtering (matches MATLAB filtfilt).
#    Use lfilter for causal filtering (matches MATLAB filter()).
#
# 5. signal.correlate needs signal.correlation_lags() separately.
#    MATLAB xcorr returns both [r, lags] in one call.
#
# 6. signal.decimate for integer downsampling (includes anti-aliasing).
#    signal.resample for arbitrary rate changes.
#
# 7. spectrogram returns (f, t, Sxx) — use pcolormesh to display,
#    not imshow, to get correct axis scaling.
