# This script creates onset files for run 1 only

import os
import numpy as np
import pandas as pd
from scipy.io import savemat
pd.options.mode.chained_assignment = None  # Disable warning

base_output_dir = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/data/onsets_0306'

# Define paths and parameters
round_num = 1
onsets_parent_path = "/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/data/onsets_type"
confounds_path = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/scratch/confounds_summary.csv'
tr = 1.12

# Load and process onset files
dataframes, empty_files = [], []

onsets_path = f"{onsets_parent_path}/R{round_num}"
for file_name in filter(lambda f: f.endswith(".txt"), os.listdir(onsets_path)):
    file_path = os.path.join(onsets_path, file_name)
    df = pd.read_csv(file_path, sep='\t', header=None, names=['onset', 'duration', 'parametric_mod'])

    if df.empty:
        empty_files.append(f'R{round_num}/{file_name}')
        continue

    df['filename'] = file_name
    df['round'] = round_num
    df['subject_id'] = df['filename'].str.extract(r'sub(\d+)').astype(int)
    df['first_pres'] = (~df['filename'].str.contains(r'\.p\.')).astype(int)
    df['stim'] = df['filename'].str.extract(r'^([^._]+)')[0]
    dataframes.append(df)

onsets_df = (
    pd.concat(dataframes, ignore_index=True)
    .query('onset != duration')
    .sort_values(['subject_id', 'round', 'onset'])
    .reset_index(drop=True)
)

# Apply mappings to add categorisations
mappings = {
    "aniweap": {
        "animals": ["cat", "goose", "lion", "grizzly"],
        "weapons": ["fist", "stick", "gun", "grenade"]
    },
    "safety": {
        "high_safety": ["cat", "goose", "gun", "grenade"],
        "low_safety": ["lion", "grizzly", "fist", "stick"]
    },
    "extint": {
        "high_external_safety": ["cat", "goose"],
        "low_external_safety": ["lion", "grizzly"],
        "high_internal_safety": ["gun", "grenade"],
        "low_internal_safety": ["fist", "stick"]
    }
}
flat_mappings = {key: {stim: category for category, stimuli in value.items() for stim in stimuli} for key, value in
                 mappings.items()}
for column, mapping in flat_mappings.items():
    onsets_df[column] = onsets_df['stim'].map(mapping)

#%% create task dataframe
onsets_df['adjusted_onset'] = onsets_df['onset']
task_df = onsets_df[['subject_id', 'adjusted_onset', 'duration']].copy()
task_df['name'] = 'task'
task_df.columns = ['subject_id', 'onset', 'duration', 'name']
condition_df = onsets_df[onsets_df['first_pres'] == 1]
conditions = ['aniweap', 'safety', 'extint']
final_dfs = {}

# Loop through conditions to create and concatenate DataFrames
for condition in conditions:
    cond_df = condition_df[['subject_id', 'adjusted_onset', 'duration', condition]].copy()
    cond_df.columns = ['subject_id', 'onset', 'duration', 'name']  # Rename columns
    final_dfs[condition] = pd.concat([cond_df, task_df], ignore_index=True)

# Access final DataFrames: final_dfs['aniweap'], final_dfs['safety'], final_dfs['extint']

#%%
mappings = {
    "aniweap": ['task', 'animals', 'weapons'],
    "safety": ['task', 'high_safety', 'low_safety'],
    "extint": ['task', 'high_external_safety', 'low_external_safety', 'high_internal_safety', 'low_internal_safety'],
}

for condition, df in final_dfs.items():
    condition_output_dir = os.path.join(base_output_dir, condition.upper())
    os.makedirs(condition_output_dir, exist_ok=True)
    custom_order = mappings[condition]
    for subject_id, group in df.groupby("subject_id"):
        names_array = np.empty((1, len(custom_order)), dtype=object)
        names_array[0, :] = custom_order
        # 2) Create 1 x N object arrays for onsets and durations
        onsets_array = np.empty((1, len(custom_order)), dtype=object)
        durations_array = np.empty((1, len(custom_order)), dtype=object)
        # 3) Fill each cell with the relevant lists
        for i, name in enumerate(custom_order):
            these_onsets = group.loc[group["name"] == name, "onset"].tolist()
            these_durations = group.loc[group["name"] == name, "duration"].tolist()
            onsets_array[0, i] = these_onsets
            durations_array[0, i] = these_durations
        # 4) Build the final dict for savemat
        mat_data = {
            "names": names_array,
            "onsets": onsets_array,
            "durations": durations_array,
        }
        # 5) Save and report
        output_path = os.path.join(condition_output_dir, f"subject_{subject_id}.mat")
        savemat(output_path, mat_data)
        print(f"Saved: {output_path}")

