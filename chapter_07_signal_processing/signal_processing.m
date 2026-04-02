% ============================================================
% Chapter 7: Signal Processing
% "From MATLAB to Python for Engineers and Scientists"
% MATLAB Reference Code
% Requires: Signal Processing Toolbox
% ============================================================

%% 7.1 Generating Test Signals
% ------------------------------------------------------------
Fs   = 1000;                        % sampling frequency (Hz)
T    = 1/Fs;                        % sampling period
t    = 0:T:1-T;                     % time vector (1 second)
N    = length(t);                   % number of samples

% Pure sine wave
f1   = 50;                          % frequency (Hz)
x1   = sin(2*pi*f1*t);

% Composite signal
f2   = 120;
x    = sin(2*pi*f1*t) + 0.5*sin(2*pi*f2*t) + 0.2*randn(size(t));

% Chirp signal (frequency sweep)
x_chirp = chirp(t, 10, 1, 200);    % 10 Hz → 200 Hz over 1 second

% Square wave
x_sq = square(2*pi*10*t);

% Plot generated signals
figure;
subplot(2,1,1)
plot(t(1:200), x(1:200))
xlabel('Time (s)'); ylabel('Amplitude')
title('Composite Signal (first 0.2s)'); grid on

subplot(2,1,2)
plot(t, x_chirp)
xlabel('Time (s)'); ylabel('Amplitude')
title('Chirp Signal'); grid on


%% 7.2 Fourier Transform and Frequency Analysis
% ------------------------------------------------------------
Fs = 1000;
t  = 0:1/Fs:1-1/Fs;
x  = sin(2*pi*50*t) + 0.5*sin(2*pi*120*t) + 0.2*randn(size(t));
N  = length(x);

% FFT
Y    = fft(x);
P2   = abs(Y/N);
P1   = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f    = Fs*(0:(N/2))/N;              % frequency axis

% Plot spectrum
figure;
plot(f, P1, 'r-', 'LineWidth', 1.5)
xlabel('Frequency (Hz)'); ylabel('|Amplitude|')
title('Single-Sided Amplitude Spectrum')
xlim([0, 300]); grid on

% Power Spectral Density (Welch method — better for noisy signals)
[pxx, f_psd] = pwelch(x, [], [], [], Fs);

figure;
semilogy(f_psd, pxx)
xlabel('Frequency (Hz)'); ylabel('PSD (V^2/Hz)')
title('Power Spectral Density (Welch)'); grid on

% Short-Time Fourier Transform (spectrogram)
figure;
spectrogram(x_chirp, 128, 120, 256, Fs, 'yaxis')
title('Spectrogram of Chirp Signal')
colorbar


%% 7.3 Digital Filters — Design and Application
% ------------------------------------------------------------
Fs = 1000;

% Low-pass Butterworth filter
% cutoff at 80 Hz, order 4
[b_lp, a_lp] = butter(4, 80/(Fs/2), 'low');

% High-pass Butterworth filter
[b_hp, a_hp] = butter(4, 30/(Fs/2), 'high');

% Band-pass filter (30–80 Hz)
[b_bp, a_bp] = butter(4, [30, 80]/(Fs/2), 'bandpass');

% Band-stop (notch) filter (45–55 Hz — remove 50 Hz noise)
[b_bs, a_bs] = butter(4, [45, 55]/(Fs/2), 'stop');

% Frequency response of low-pass filter
figure;
freqz(b_lp, a_lp, 1024, Fs)
title('Low-Pass Butterworth Filter Response')

% Apply filter to signal
t = 0:1/Fs:1-1/Fs;
x = sin(2*pi*50*t) + sin(2*pi*200*t) + 0.2*randn(size(t));

x_filt_lp = filtfilt(b_lp, a_lp, x);    % zero-phase filtering
x_filt_hp = filtfilt(b_hp, a_hp, x);

% Compare original and filtered
figure;
subplot(3,1,1); plot(t(1:200), x(1:200));        title('Original');   grid on
subplot(3,1,2); plot(t(1:200), x_filt_lp(1:200)); title('Low-pass filtered'); grid on
subplot(3,1,3); plot(t(1:200), x_filt_hp(1:200)); title('High-pass filtered'); grid on


%% 7.4 FIR Filters
% ------------------------------------------------------------
Fs = 1000;

% FIR low-pass filter using window method
order = 64;                         % filter order
fc    = 80;                         % cutoff frequency (Hz)
b_fir = fir1(order, fc/(Fs/2), 'low');  % Hamming window by default

% Apply FIR filter
t = 0:1/Fs:1-1/Fs;
x = sin(2*pi*50*t) + sin(2*pi*200*t) + 0.2*randn(size(t));
x_fir = filtfilt(b_fir, 1, x);

% FIR filter frequency response
figure;
freqz(b_fir, 1, 1024, Fs)
title('FIR Low-Pass Filter Response')


%% 7.5 Correlation and Convolution
% ------------------------------------------------------------
Fs = 1000;
t  = 0:1/Fs:1-1/Fs;
x  = sin(2*pi*5*t) + 0.5*randn(size(t));
y  = circshift(x, 50) + 0.3*randn(size(t));    % delayed version of x

% Cross-correlation (find delay between signals)
[r, lags] = xcorr(x, y, 'coeff');
[~, idx]  = max(r);
delay_samples = lags(idx);
delay_ms      = delay_samples / Fs * 1000;
fprintf('Detected delay: %.1f ms\n', delay_ms)

% Auto-correlation
[r_auto, lags_auto] = xcorr(x, x, 'coeff');

% Convolution
h   = ones(1, 20) / 20;            % moving average filter kernel
y_c = conv(x, h, 'same');          % SAME: output same length as input

figure;
subplot(2,1,1)
plot(lags/Fs*1000, r)
xlabel('Lag (ms)'); ylabel('Correlation')
title('Cross-Correlation'); grid on

subplot(2,1,2)
plot(t(1:200), x(1:200)); hold on
plot(t(1:200), y_c(1:200)); hold off
legend('Original','Smoothed')
title('Convolution (Moving Average)'); grid on


%% 7.6 Resampling
% ------------------------------------------------------------
Fs_orig = 1000;
t_orig  = 0:1/Fs_orig:1-1/Fs_orig;
x_orig  = sin(2*pi*50*t_orig) + 0.1*randn(size(t_orig));

% Downsample by factor of 4 (1000 Hz → 250 Hz)
x_down = downsample(x_orig, 4);
Fs_down = Fs_orig / 4;

% Resample to 500 Hz (proper anti-aliasing included)
[x_re, t_re] = resample(x_orig, 500, Fs_orig);

% Upsample
x_up = upsample(x_orig, 2);


%% 7.7 Real Engineering Case: Vibration Analysis
% ------------------------------------------------------------
% Typical workflow: acquire signal → filter → FFT → identify frequencies
% Application: rotating machinery fault detection

Fs   = 5000;                        % 5 kHz sampling rate
t    = 0:1/Fs:2-1/Fs;              % 2 seconds
N    = length(t);

% Simulate vibration signal
f_rot  = 25;                        % rotation frequency (Hz) — 1500 RPM
f_fault = f_rot * 3.5;             % bearing fault frequency

x_vib = (1.0 * sin(2*pi*f_rot*t)   ...   % fundamental
        + 0.4 * sin(2*pi*2*f_rot*t) ...   % 2nd harmonic
        + 0.2 * sin(2*pi*f_fault*t) ...   % fault frequency
        + 0.5 * randn(size(t)));           % broadband noise

% Step 1: Band-pass filter (5–500 Hz)
[b, a]   = butter(4, [5, 500]/(Fs/2), 'bandpass');
x_filt   = filtfilt(b, a, x_vib);

% Step 2: FFT of filtered signal
Y    = fft(x_filt);
P2   = abs(Y/N);
P1   = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f_ax = Fs*(0:(N/2))/N;

% Step 3: PSD via Welch for better frequency resolution
[pxx, f_psd] = pwelch(x_filt, 2048, 1024, 4096, Fs);

% Plot results
figure;
subplot(3,1,1)
plot(t(1:500), x_vib(1:500))
xlabel('Time (s)'); ylabel('Acceleration (g)')
title('Raw Vibration Signal'); grid on

subplot(3,1,2)
plot(f_ax, P1, 'b-')
xlabel('Frequency (Hz)'); ylabel('|Amplitude|')
title('FFT Spectrum'); xlim([0, 300]); grid on
xline(f_rot,   'r--', 'LineWidth',1.5, 'Label','1×')
xline(2*f_rot, 'g--', 'LineWidth',1.5, 'Label','2×')
xline(f_fault, 'm--', 'LineWidth',1.5, 'Label','Fault')

subplot(3,1,3)
semilogy(f_psd, pxx, 'k-')
xlabel('Frequency (Hz)'); ylabel('PSD')
title('Welch PSD'); xlim([0, 300]); grid on

sgtitle('Vibration Analysis: Rotating Machinery')
