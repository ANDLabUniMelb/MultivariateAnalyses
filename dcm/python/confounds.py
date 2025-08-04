import pandas as pd

IN_FILE  = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm_7t/data/sub-15_task-safety_run-4_desc-confounds_timeseries.tsv'
OUT_FILE = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm_7t/data/s_sub-15_task-safety_run-4_desc-confounds_timeseries.txt'

cols = [
    'trans_x','trans_x_derivative1','trans_x_power2','trans_x_derivative1_power2',
    'trans_y','trans_y_derivative1','trans_y_power2','trans_y_derivative1_power2',
    'trans_z','trans_z_derivative1','trans_z_power2','trans_z_derivative1_power2',
    'rot_x','rot_x_derivative1','rot_x_power2','rot_x_derivative1_power2',
    'rot_y','rot_y_derivative1','rot_y_power2','rot_y_derivative1_power2',
    'rot_z','rot_z_derivative1','rot_z_power2','rot_z_derivative1_power2'
]

# 1 & 2.  Read only the required columns
df = pd.read_csv(IN_FILE, sep='\t', usecols=cols)

# 3.  Forward-fill then backward-fill any remaining NaNs
df = df.ffill().bfill()

# 4.  Write without header or index, tab-separated
df.to_csv(OUT_FILE, sep='\t', index=False, header=False)