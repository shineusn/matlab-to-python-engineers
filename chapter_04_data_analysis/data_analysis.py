# ============================================================
# Chapter 4: Data Handling and Analysis with pandas
# "From MATLAB to Python for Engineers and Scientists"
# Python Reference Code
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 4.1 Creating DataFrames
# ============================================================
# pandas DataFrame is the Python equivalent of MATLAB table.
# It is the single most important tool for data work in Python.

# Create DataFrame from a dictionary — most common way
data = {
    'Name':       ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'Age':        [25, 30, 35, 28, 32],
    'Salary':     [50000, 62000, 75000, 58000, 71000],
    'Department': ['Engineering', 'Marketing', 'Engineering', 'HR', 'Marketing']
}

df = pd.DataFrame(data)
print(df)

# MATLAB: T = table(name, age, salary, dept, 'VariableNames', {...})
# Python: df = pd.DataFrame({'col1': array1, 'col2': array2, ...})

# Create from NumPy array
arr = np.random.rand(4, 3)
df2 = pd.DataFrame(arr, columns=['A', 'B', 'C'])


# ============================================================
# 4.2 Reading and Writing Data Files
# ============================================================

# Read CSV
df_csv = pd.read_csv('employees.csv')               # MATLAB: readtable('employees.csv')

# Read Excel
df_xl  = pd.read_excel('employees.xlsx',
                        sheet_name='Sheet1')         # MATLAB: readtable(...,'Sheet','Sheet1')

# Write CSV
df.to_csv('output.csv', index=False)                # MATLAB: writetable(T,'output.csv')
# index=False avoids writing row numbers as a column — almost always what you want

# Write Excel
df.to_excel('output.xlsx', sheet_name='Results',
            index=False)                             # MATLAB: writetable(T,'output.xlsx',...)

# Read plain numeric data (no headers)
arr = np.loadtxt('data.csv', delimiter=',')         # MATLAB: readmatrix('data.csv')

# *** Common trap: forgetting index=False in to_csv ***
# df.to_csv('out.csv')          writes row numbers 0,1,2... as first column
# df.to_csv('out.csv', index=False)  clean output matching MATLAB writetable


# ============================================================
# 4.3 Inspecting Data
# ============================================================

print(df.head(3))           # MATLAB: head(T,3)
print(df.tail(3))           # MATLAB: tail(T,3)
print(df.shape)             # MATLAB: size(T)  → (rows, cols)
print(df.columns.tolist())  # MATLAB: T.Properties.VariableNames
print(df.dtypes)            # MATLAB: (no direct equivalent)
print(df.info())            # shows dtypes + non-null counts — very useful
print(df.describe())        # MATLAB: summary(T) — stats for numeric columns


# ============================================================
# 4.4 Selecting and Filtering Data
# ============================================================

# Select a single column — returns a Series (1D)
ages = df['Age']                        # MATLAB: T.Age
# OR using dot notation (only works if column name has no spaces)
ages = df.Age

# Select multiple columns — returns a DataFrame
df_sub = df[['Name', 'Salary']]         # MATLAB: T(:,{'Name','Salary'})

# Select rows by condition (boolean indexing)
df_eng  = df[df['Department'] == 'Engineering']     # MATLAB: T(strcmp(T.Dept,'Engineering'),:)
df_high = df[df['Salary'] > 60000]                  # MATLAB: T(T.Salary > 60000,:)

# Combined conditions — use & and | with parentheses
df_filt = df[(df['Department'] == 'Engineering') & (df['Age'] < 35)]
# MATLAB: T(strcmp(T.Dept,'Engineering') & T.Age < 35, :)

# *** Critical trap: use & not 'and' for DataFrame conditions ***
# df[df['A'] > 1 and df['B'] > 2]   → ERROR (Python 'and' doesn't work here)
# df[(df['A'] > 1) & (df['B'] > 2)] → correct  (bitwise & on boolean arrays)
# Always wrap each condition in parentheses!

# .loc — label-based selection (rows and columns by name)
df_loc = df.loc[0:2, ['Name', 'Age']]   # rows 0-2, specific columns
                                         # Note: loc includes endpoint (0,1,2)

# .iloc — integer position-based selection (like MATLAB indexing)
df_iloc = df.iloc[0:2, 0:2]            # first 2 rows, first 2 cols
                                        # Note: iloc excludes endpoint (0,1 only)

# *** loc vs iloc endpoint rule ***
# df.loc[0:2]   → rows 0, 1, 2  (endpoint INCLUDED — unusual for Python)
# df.iloc[0:2]  → rows 0, 1     (endpoint EXCLUDED — standard Python)


# ============================================================
# 4.5 Adding and Modifying Columns
# ============================================================

# Add new column
df['Bonus'] = df['Salary'] * 0.1           # MATLAB: T.Bonus = T.Salary * 0.1

# Conditional column with np.where (MATLAB: ifelse-style)
df['Level'] = np.where(df['Salary'] > 65000, 'Senior', 'Junior')

# Modify existing column
df['Age'] = df['Age'] + 1                  # MATLAB: T.Age = T.Age + 1

# Rename columns
df = df.rename(columns={'Bonus': 'AnnualBonus'})   # MATLAB: T.Properties.VariableNames{...}

# Drop columns
df = df.drop(columns=['AnnualBonus', 'Level'])      # MATLAB: T.ColumnName = []


# ============================================================
# 4.6 Sorting
# ============================================================

# Sort by one column
df_sorted      = df.sort_values('Salary')                      # MATLAB: sortrows(T,'Salary')
df_sorted_desc = df.sort_values('Salary', ascending=False)     # descending

# Sort by multiple columns
df_multi = df.sort_values(['Department', 'Salary'],
                           ascending=[True, False])
# MATLAB: sortrows(T, {'Department','Salary'})

# Reset index after sorting (good practice)
df_sorted = df_sorted.reset_index(drop=True)
# Without this, original row numbers are preserved — can cause confusion


# ============================================================
# 4.7 Grouping and Aggregation
# ============================================================
# groupby is one of pandas' most powerful features.
# MATLAB equivalent: findgroups + splitapply (much more verbose)

# Group by one column, compute mean
dept_mean = df.groupby('Department')['Salary'].mean()
print(dept_mean)
# MATLAB: splitapply(@mean, T.Salary, findgroups(T.Department))

# Multiple aggregations at once
dept_stats = df.groupby('Department')['Salary'].agg(['mean', 'std', 'count'])
print(dept_stats)

# Group by multiple columns
multi_group = df.groupby(['Department', 'Age'])['Salary'].mean()

# Apply different functions to different columns
agg_result = df.groupby('Department').agg({
    'Salary': 'mean',
    'Age':    'max'
})
print(agg_result)

# Count rows per group
counts = df.groupby('Department').size()    # MATLAB: splitapply(@numel,...)
print(counts)


# ============================================================
# 4.8 Handling Missing Data
# ============================================================

# Create DataFrame with missing values (NaN)
df_miss = pd.DataFrame({
    'A': [1.0, np.nan, 3.0, np.nan, 5.0],
    'B': [10.0, 20.0, np.nan, 40.0, 50.0]
})

# Detect missing values
print(df_miss.isna())           # MATLAB: isnan(v)
print(df_miss.isna().sum())     # count missing per column

# Drop rows with ANY missing value
df_dropped = df_miss.dropna()           # MATLAB: v(~isnan(v))

# Drop rows only if ALL values are missing
df_dropped2 = df_miss.dropna(how='all')

# Fill missing with a constant
df_filled = df_miss.fillna(0)           # MATLAB: v(isnan(v)) = 0

# Fill missing with column mean
df_filled2 = df_miss.fillna(df_miss.mean())
# MATLAB: v(isnan(v)) = mean(v,'omitnan')

# Forward fill (propagate last valid value forward)
df_ffill = df_miss.ffill()

# *** isna() vs isnan() ***
# np.isnan() works on NumPy arrays
# df.isna()  works on DataFrames and handles non-numeric NaN too
# Use df.isna() when working with DataFrames


# ============================================================
# 4.9 Merging DataFrames
# ============================================================

df1 = pd.DataFrame({
    'Name':   ['Alice', 'Bob', 'Charlie'],
    'DeptID': [1, 2, 3]
})
df2 = pd.DataFrame({
    'DeptID':   [1, 2, 3],
    'DeptName': ['Engineering', 'Marketing', 'HR']
})

# Inner join — keeps only matching rows
df_inner = pd.merge(df1, df2, on='DeptID', how='inner')
# MATLAB: innerjoin(T1, T2, 'Keys', 'DeptID')

# Left join — keeps all rows from left DataFrame
df_left = pd.merge(df1, df2, on='DeptID', how='left')
# MATLAB: outerjoin(T1, T2, 'Keys', 'DeptID', 'Type', 'left', ...)

# Merge on columns with different names
df_right_renamed = df2.rename(columns={'DeptID': 'ID'})
df_merged = pd.merge(df1, df_right_renamed,
                     left_on='DeptID', right_on='ID')

print(df_inner)


# ============================================================
# 4.10 Real Engineering Data Workflow
# ============================================================
# Sensor time-series data processing — a workflow you will use
# constantly when analyzing experimental or simulation results.

# Generate sample sensor data
rng    = np.random.default_rng(seed=0)
t      = np.arange(0, 10, 0.01)                            # 0 to 10 s
signal = np.sin(2 * np.pi * 0.5 * t) + 0.1 * rng.standard_normal(len(t))
temp   = 20 + 5 * np.sin(2 * np.pi * 0.1 * t) + 0.5 * rng.standard_normal(len(t))

# Build DataFrame
sensor_df = pd.DataFrame({
    'Time_s':         t,
    'Signal':         signal,
    'Temperature_C':  temp
})

# Add smoothed signal (rolling mean — like MATLAB movmean)
sensor_df['Signal_Smoothed'] = sensor_df['Signal'].rolling(
    window=20, center=True).mean()
# MATLAB: movmean(signal, 20)

# Filter to a time window
window = sensor_df[
    (sensor_df['Time_s'] >= 2) & (sensor_df['Time_s'] <= 8)
].copy()

# Bin by whole seconds and compute statistics per bin
sensor_df['TimeBin'] = sensor_df['Time_s'].astype(int)
bin_stats = sensor_df.groupby('TimeBin')['Signal'].agg(['mean', 'std'])
print(bin_stats)

# Summary statistics
print(f"\nMean signal : {sensor_df['Signal'].mean():.4f}")
print(f"Std  signal : {sensor_df['Signal'].std():.4f}")
print(f"Data points : {len(sensor_df)}")

# Plot raw vs smoothed
fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

axes[0].plot(sensor_df['Time_s'], sensor_df['Signal'],
             alpha=0.4, color='steelblue', label='Raw')
axes[0].plot(sensor_df['Time_s'], sensor_df['Signal_Smoothed'],
             color='navy', linewidth=2, label='Smoothed')
axes[0].set_ylabel('Signal'); axes[0].legend(); axes[0].grid(True)

axes[1].plot(sensor_df['Time_s'], sensor_df['Temperature_C'],
             color='coral', linewidth=1.5)
axes[1].set_ylabel('Temperature (°C)'); axes[1].set_xlabel('Time (s)')
axes[1].grid(True)

plt.suptitle('Sensor Data Analysis', fontsize=13)
plt.tight_layout()
plt.savefig('sensor_analysis.png', dpi=150)
plt.show()


# ============================================================
# Chapter 4 Summary: Key Differences to Remember
# ============================================================
#
# 1. COLUMN SELECTION uses brackets not dot for safety:
#    df['Column']  not  df.Column  (dot fails if name has spaces)
#
# 2. BOOLEAN CONDITIONS need & not 'and', with parentheses:
#    df[(df['A'] > 1) & (df['B'] < 5)]  — not  df[df['A']>1 and ...]
#
# 3. loc INCLUDES endpoint, iloc EXCLUDES it:
#    df.loc[0:2]  → rows 0,1,2
#    df.iloc[0:2] → rows 0,1
#
# 4. to_csv needs index=False to match MATLAB writetable output.
#
# 5. groupby replaces findgroups+splitapply — much more concise.
#
# 6. Use df.isna() for DataFrames, np.isnan() for NumPy arrays.
#
# 7. std() default matches MATLAB: pandas uses ddof=1 by default.
