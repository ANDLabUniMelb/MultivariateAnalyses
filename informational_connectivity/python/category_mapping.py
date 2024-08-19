import os
import re
import pandas as pd

# Define the directory containing the files
directory = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/data/Joe_secondstim'

# Initialize an empty dictionary to store the mappings
name_to_direction = {}

# Loop through each file in the directory
# List of valid stimulus names
stimulus_names = ["cat", "fist", "goose", "grenade", "grizzly", "gun", "lion", "stick"]

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.startswith('second_probchange_') and filename.endswith('.txt'):
        # Extract the stimulus name from the filename
        stimulus_name = filename.split('_')[-1].replace('.txt', '')

        # Check if the stimulus name is valid
        if stimulus_name in stimulus_names:
            # Construct the full file path
            filepath = os.path.join(directory, filename)

            # Read the file into a pandas DataFrame
            df = pd.read_csv(filepath, delimiter='\t')

            # Extract the order and second.direction columns
            orders = df['order'].tolist()
            directions = df['second.direction'].tolist()

            # Generate the name based on the filename and order
            base_name = filename.replace('second_probchange_', '').replace('.txt', '')
            for order, direction in zip(orders, directions):
                name = f"{base_name}{order}"
                name_to_direction[name] = direction


def convert_key_format(original_dict):
    new_dict = {}
    for key, value in original_dict.items():
        parts = key.split('_')
        sub_part = parts[0][3:]  # Get the number after 'sub'
        run_part = parts[1]  # Get the R part
        stimulus_match = re.match(r"([a-zA-Z]+)(\d+)", parts[2])  # Match the stimulus type and index
        if stimulus_match:
            stimulus_type = stimulus_match.group(1)  # Get the stimulus type part
            stimulus_index = stimulus_match.group(2)  # Get the stimulus index part
            new_key = f"{run_part}_{stimulus_type}_sub{sub_part}_{stimulus_type}{stimulus_index}.nii.gz"
            new_value = 2 if value == -1 else value  # Map -1 to 2
            new_dict[new_key] = new_value
    return new_dict
# Convert the dictionary
name_to_direction = convert_key_format(name_to_direction)


# If you want to save it as a CSV file
df_output = pd.DataFrame(list(name_to_direction.items()), columns=["filename", "direction"])
df_output = df_output.sort_values(by = 'filename').reset_index(drop = True)
df_output.to_csv('/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/data/direction_lookup.csv', index=False)