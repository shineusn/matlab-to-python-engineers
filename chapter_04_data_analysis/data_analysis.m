% ============================================================
% Chapter 4: Data Handling and Analysis
% "From MATLAB to Python for Engineers and Scientists"
% MATLAB Reference Code
% ============================================================

%% 4.1 Creating Tables
% ------------------------------------------------------------
% MATLAB table is the closest equivalent to pandas DataFrame

% Create table from arrays
name   = {'Alice'; 'Bob'; 'Charlie'; 'Diana'; 'Eve'};
age    = [25; 30; 35; 28; 32];
salary = [50000; 62000; 75000; 58000; 71000];
dept   = {'Engineering'; 'Marketing'; 'Engineering'; 'HR'; 'Marketing'};

T = table(name, age, salary, dept, ...
    'VariableNames', {'Name','Age','Salary','Department'});

disp(T)


%% 4.2 Reading and Writing Data Files
% ------------------------------------------------------------

% Read CSV
T_csv = readtable('employees.csv');

% Read Excel
T_xl  = readtable('employees.xlsx', 'Sheet', 'Sheet1');

% Write CSV
writetable(T, 'output.csv');

% Write Excel
writetable(T, 'output.xlsx', 'Sheet', 'Results');

% Read plain numeric matrix from CSV (no headers)
M = readmatrix('data.csv');

% Write plain numeric matrix
writematrix(M, 'matrix_out.csv');


%% 4.3 Inspecting Data
% ------------------------------------------------------------
% Basic inspection
disp(head(T, 3))        % first 3 rows
disp(tail(T, 3))        % last 3 rows
disp(size(T))           % [rows, cols]
disp(T.Properties.VariableNames)    % column names

% Summary statistics
summary(T)


%% 4.4 Selecting and Filtering Data
% ------------------------------------------------------------

% Select a single column (returns array)
ages = T.Age;

% Select multiple columns (returns table)
T_sub = T(:, {'Name', 'Salary'});

% Select rows by condition
T_eng  = T(strcmp(T.Department, 'Engineering'), :);
T_high = T(T.Salary > 60000, :);

% Combined condition
T_filt = T(strcmp(T.Department, 'Engineering') & T.Age < 35, :);

% Select by row index
T_first2 = T(1:2, :);


%% 4.5 Adding and Modifying Columns
% ------------------------------------------------------------

% Add new column
T.SeniorityBonus = T.Salary * 0.1;

% Modify existing column
T.Age = T.Age + 1;     % birthday for everyone

% Rename column
T.Properties.VariableNames{'SeniorityBonus'} = 'Bonus';

% Remove column
T.Bonus = [];


%% 4.6 Sorting
% ------------------------------------------------------------

% Sort by one column
T_sorted = sortrows(T, 'Salary');               % ascending
T_sorted_desc = sortrows(T, 'Salary', 'descend');

% Sort by multiple columns
T_multi = sortrows(T, {'Department', 'Salary'});


%% 4.7 Grouping and Aggregation
% ------------------------------------------------------------

% Group by Department, compute mean salary
dept_groups = findgroups(T.Department);
dept_names  = unique(T.Department);
mean_salary = splitapply(@mean, T.Salary, dept_groups);

% Display result
result = table(dept_names, mean_salary, ...
    'VariableNames', {'Department', 'MeanSalary'});
disp(result)

% Count per group
counts = splitapply(@numel, T.Salary, dept_groups);


%% 4.8 Handling Missing Data
% ------------------------------------------------------------

% Create data with missing values
v = [1; NaN; 3; NaN; 5];

% Detect missing
missing_mask = isnan(v);

% Remove missing
v_clean = v(~isnan(v));

% Replace missing with mean
v_filled = v;
v_filled(isnan(v_filled)) = mean(v_filled, 'omitnan');

% Count missing values
n_missing = sum(isnan(v));
fprintf('Missing values: %d\n', n_missing)


%% 4.9 Merging Tables
% ------------------------------------------------------------

% Create two tables to join
T1 = table({'Alice';'Bob';'Charlie'}, [1;2;3], ...
    'VariableNames', {'Name','DeptID'});
T2 = table([1;2;3], {'Engineering';'Marketing';'HR'}, ...
    'VariableNames', {'DeptID','DeptName'});

% Inner join (keeps only matching rows)
T_joined = innerjoin(T1, T2, 'Keys', 'DeptID');
disp(T_joined)

% Left join (keeps all rows from T1)
T_left = outerjoin(T1, T2, 'Keys', 'DeptID', 'Type', 'left', ...
    'MergeKeys', true);


%% 4.10 Real Engineering Data Workflow
% ------------------------------------------------------------
% Simulate a typical sensor data processing workflow

% Generate sample sensor data (time series)
t        = (0:0.01:10)';           % time vector, 0 to 10 seconds
signal   = sin(2*pi*0.5*t) + 0.1*randn(size(t));  % noisy sine wave
temp     = 20 + 5*sin(2*pi*0.1*t) + 0.5*randn(size(t));

% Create table
sensor_data = table(t, signal, temp, ...
    'VariableNames', {'Time_s', 'Signal', 'Temperature_C'});

% Add derived column
sensor_data.Signal_Smoothed = movmean(sensor_data.Signal, 20);

% Filter to a time window
window = sensor_data(sensor_data.Time_s >= 2 & ...
                     sensor_data.Time_s <= 8, :);

% Summary statistics per second (bin by floor of time)
sensor_data.TimeBin = floor(sensor_data.Time_s);
bins     = findgroups(sensor_data.TimeBin);
bin_mean = splitapply(@mean, sensor_data.Signal, bins);
bin_std  = splitapply(@std,  sensor_data.Signal, bins);

fprintf('Mean signal: %.4f\n', mean(sensor_data.Signal))
fprintf('Std  signal: %.4f\n', std(sensor_data.Signal))
