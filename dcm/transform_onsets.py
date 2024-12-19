#%%
import pandas as pd
import os

# Define the data directory
data_dir = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/data/test_data'

# Define the mappings for each group
mappings = {
    "ANIWEAP": {
        "animals": ["cat", "goose", "lion", "grizzly"],
        "weapons": ["fist", "stick", "gun", "grenade"]
    },
    "SAFETY": {
        "high_safety": ["cat", "goose", "gun", "grenade"],
        "low_safety": ["lion", "grizzly", "fist", "stick"]
    },
    "EXTINT": {
        "high_external_safety": ["cat", "goose"],
        "low_external_safety": ["lion", "grizzly"],
        "high_internal_safety": ["gun", "grenade"],
        "low_internal_safety": ["fist", "stick"]
    }
}

# Process files for subjects 1 to 31
for subject_id in range(1, 32):
    onset_file = f"{data_dir}/combined_second_onsets/combined_onsets_sub_{subject_id}.txt"

    # Load the onset file
    if not os.path.exists(onset_file):
        print(f"File not found: {onset_file}")
        continue

    data = pd.read_csv(onset_file, sep="\t", names=["onset", "duration", "stimulus"])

    # Process each group
    for group, conditions in mappings.items():
        group_transformed = []
        for condition, stimuli in conditions.items():
            # Filter rows matching the stimuli for this condition
            condition_data = data[data["stimulus"].isin(stimuli)].copy()
            condition_data["condition"] = condition  # Add condition label
            group_transformed.append(condition_data)

        # Combine all transformations for this group
        group_data = pd.concat(group_transformed)

        # Sort by onset time
        group_data = group_data.sort_values(by="onset")

        # Drop the stimulus column
        group_data = group_data.drop(columns=['stimulus'])

        # Save to file with subject ID in filename
        os.makedirs(f"{data_dir}/transformed_second_onsets_{group}", exist_ok=True)
        group_output_file = f"{data_dir}/transformed_second_onsets_{group}/onsets_sub_{subject_id}.txt"
        group_data.to_csv(group_output_file, sep="\t", index=False, header=False)
        print(f"Onsets saved for subject {subject_id}, {group}: {group_output_file}")

#%%
