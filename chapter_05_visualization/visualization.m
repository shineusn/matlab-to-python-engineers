% ============================================================
% Chapter 5: Visualization – From MATLAB Plots to Python Figures
% "From MATLAB to Python for Engineers and Scientists"
% MATLAB Reference Code
% ============================================================

%% 5.1 Basic Line and Scatter Plots
% ------------------------------------------------------------
x = linspace(0, 2*pi, 100);
y1 = sin(x);
y2 = cos(x);

% Simple line plot
figure;
plot(x, y1)
xlabel('x')
ylabel('y')
title('Sine Wave')
grid on

% Multiple lines on same axes
figure;
plot(x, y1, 'b-',  'LineWidth', 2, 'DisplayName', 'sin(x)')
hold on
plot(x, y2, 'r--', 'LineWidth', 2, 'DisplayName', 'cos(x)')
hold off
xlabel('x'); ylabel('y')
title('Sine and Cosine')
legend('Location', 'best')
grid on

% Scatter plot
rng(0);
x_sc = randn(1, 100);
y_sc = 2*x_sc + randn(1, 100);

figure;
scatter(x_sc, y_sc, 40, 'filled', 'MarkerFaceAlpha', 0.6)
xlabel('x'); ylabel('y')
title('Scatter Plot')
grid on


%% 5.2 Subplots
% ------------------------------------------------------------
figure;

subplot(2, 2, 1)
plot(x, sin(x), 'b-', 'LineWidth', 1.5)
title('sin(x)'); grid on

subplot(2, 2, 2)
plot(x, cos(x), 'r-', 'LineWidth', 1.5)
title('cos(x)'); grid on

subplot(2, 2, 3)
plot(x, sin(2*x), 'g-', 'LineWidth', 1.5)
title('sin(2x)'); grid on

subplot(2, 2, 4)
plot(x, cos(2*x), 'm-', 'LineWidth', 1.5)
title('cos(2x)'); grid on

sgtitle('Trigonometric Functions')     % overall figure title


%% 5.3 Bar, Histogram, and Box Plots
% ------------------------------------------------------------

% Bar chart
categories = {'Jan','Feb','Mar','Apr','May'};
values     = [23, 31, 28, 35, 42];

figure;
bar(values)
set(gca, 'XTickLabel', categories)
xlabel('Month'); ylabel('Sales')
title('Monthly Sales'); grid on

% Grouped bar chart
data_grouped = [23, 20; 31, 28; 28, 25; 35, 30; 42, 38];

figure;
bar(data_grouped)
set(gca, 'XTickLabel', categories)
legend('Product A', 'Product B')
xlabel('Month'); ylabel('Sales')
title('Monthly Sales by Product')
grid on

% Histogram
data_hist = randn(1, 1000);

figure;
histogram(data_hist, 30)
xlabel('Value'); ylabel('Count')
title('Histogram of Normal Distribution')
grid on

% Box plot
group1 = randn(1, 50);
group2 = randn(1, 50) + 1;
group3 = randn(1, 50) - 1;

figure;
boxplot([group1', group2', group3'], ...
    'Labels', {'Group A', 'Group B', 'Group C'})
ylabel('Value')
title('Box Plot Comparison')
grid on


%% 5.4 Heatmaps and Contour Plots
% ------------------------------------------------------------

% Heatmap / image of a matrix
[X, Y] = meshgrid(-3:0.1:3, -3:0.1:3);
Z = exp(-(X.^2 + Y.^2));   % 2D Gaussian

figure;
imagesc(Z)
colorbar
title('Heatmap: 2D Gaussian')
axis equal tight

% Contour plot
figure;
contourf(X, Y, Z, 20)
colorbar
xlabel('x'); ylabel('y')
title('Filled Contour Plot')

% 3D surface
figure;
surf(X, Y, Z)
colorbar
xlabel('x'); ylabel('y'); zlabel('z')
title('3D Surface Plot')
shading interp


%% 5.5 Customizing Appearance
% ------------------------------------------------------------
figure;
plot(x, sin(x), 'Color', [0.2, 0.4, 0.8], ...
    'LineWidth', 2.5, ...
    'LineStyle', '-', ...
    'Marker', 'o', ...
    'MarkerSize', 4, ...
    'MarkerIndices', 1:10:length(x))

% Axis limits
xlim([0, 2*pi])
ylim([-1.2, 1.2])

% Font size
set(gca, 'FontSize', 12)

% Tick customization
xticks([0, pi/2, pi, 3*pi/2, 2*pi])
xticklabels({'0', '\pi/2', '\pi', '3\pi/2', '2\pi'})

xlabel('Angle (rad)', 'FontSize', 13)
ylabel('Amplitude',   'FontSize', 13)
title('Customized Sine Wave', 'FontSize', 14)
grid on; box on


%% 5.6 Saving Figures
% ------------------------------------------------------------
fig = figure;
plot(x, sin(x), 'b-', 'LineWidth', 2)
title('Saved Figure')
grid on

% Save as PNG (high resolution)
saveas(fig, 'sine_wave.png')

% Save as PDF (vector format — best for publications)
exportgraphics(fig, 'sine_wave.pdf', 'ContentType', 'vector')

% Save as EPS
exportgraphics(fig, 'sine_wave.eps', 'ContentType', 'vector')


%% 5.7 Engineering Plot: Signal Analysis
% ------------------------------------------------------------
% Time domain + frequency domain — common in engineering work

Fs   = 1000;                    % sampling frequency (Hz)
t_s  = 0:1/Fs:1-1/Fs;          % time vector (1 second)
f1   = 50;  f2 = 120;           % signal frequencies
sig  = sin(2*pi*f1*t_s) + 0.5*sin(2*pi*f2*t_s) + 0.2*randn(size(t_s));

% FFT
N    = length(sig);
Y    = fft(sig);
P2   = abs(Y/N);
P1   = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f_ax = Fs*(0:(N/2))/N;

figure;
subplot(2,1,1)
plot(t_s(1:200), sig(1:200), 'b-')
xlabel('Time (s)'); ylabel('Amplitude')
title('Time Domain Signal'); grid on

subplot(2,1,2)
plot(f_ax, P1, 'r-', 'LineWidth', 1.5)
xlabel('Frequency (Hz)'); ylabel('|Amplitude|')
title('Frequency Spectrum (FFT)'); grid on
xlim([0, 200])
