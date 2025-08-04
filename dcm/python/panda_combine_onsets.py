import pandas as pd
from pathlib import Path

# Set input and output directories
input_dir = Path("/Users/joecussen/Documents/Jobs/unimelb/projects/panda/data/fear2_onsets")
output_dir = Path("/Users/joecussen/Documents/Jobs/unimelb/projects/panda/data/fear2_combined_onsets")
output_dir.mkdir(parents=True, exist_ok=True)  # create if it doesn't exist

# Define file pairs
pairs = [
    ("CS-_earlyRe-extinction.txt", "CS-_lateRe-extinction.txt", "CS-_Re-extinction.txt"),
    ("CS+_earlyRe-extinction.txt", "CS+_lateRe-extinction.txt", "CS+_Re-extinction.txt"),
]

# Process each file pair
for early_file, late_file, output_file in pairs:
    early_path = input_dir / early_file
    late_path = input_dir / late_file
    output_path = output_dir / output_file

    df_early = pd.read_csv(early_path, delim_whitespace=True, header=None)
    df_late = pd.read_csv(late_path, delim_whitespace=True, header=None)

    df_combined = pd.concat([df_early, df_late]).sort_values(by=0).reset_index(drop=True)
    df_combined.to_csv(output_path, sep='\t', header=False, index=False)