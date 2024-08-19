import pandas as pd
import numpy as np
import nibabel as nib
from scipy.stats import pearsonr, zscore

def load_and_mask_data(files, roi_masks, trial_dir):
    print('loading all data')
    masks = {}
    for roi_name, mask_path in roi_masks.items():
        try:
            mask_img = nib.load(mask_path)
            masks[roi_name] = mask_img.get_fdata().astype(bool)
        except Exception as e:
            print(f"Error loading mask {mask_path}: {e}")
            masks[roi_name] = None

    data = {}
    for file in files:
        try:
            img = nib.load(f'{trial_dir}/{file}')
            img_data = img.get_fdata()
        except Exception as e:
            print(f"Error loading file {file}: {e}")
            for roi_name in roi_masks.keys():
                data[(file, roi_name)] = None
            continue  # Skip this file if it cannot be loaded

        for roi_name, mask in masks.items():
            if mask is not None:
                try:
                    masked_data = img_data[mask]
                    if np.any(masked_data):
                        data[(file, roi_name)] = masked_data
                        print(f"File {file} successfully processed with ROI mask {roi_name}.")
                    else:
                        data[(file, roi_name)] = None
                        print(f"All zero data for file {file} with ROI mask {roi_name}.")
                except Exception as e:
                    print(f"Error applying mask to file {file} with ROI mask {roi_name}: {e}")
                    data[(file, roi_name)] = None
            else:
                data[(file, roi_name)] = None
                print(f"Mask data unavailable for ROI {roi_name}, skipping file {file}.")
    return data



def compute_correlations(df_pairs, preprocessed_data, roi_masks):
    for roi_name in roi_masks.keys():
        correlations = []
        for idx, row in df_pairs.iterrows():
            data1 = preprocessed_data.get((row['filename_1'], roi_name), None)
            data2 = preprocessed_data.get((row['filename_2'], roi_name), None)

            if data1 is None or data2 is None:
                print(f"Missing data for {row['filename_1']} and {row['filename_2']} with ROI {roi_name}.")
                correlations.append(np.nan)
            else:
                # Normalize data with z-score
                try:
                    normalized_data1 = zscore(data1)
                    normalized_data2 = zscore(data2)
                    correlation, _ = pearsonr(normalized_data1, normalized_data2)
                    correlations.append(correlation)
                except Exception as e:
                    print(
                        f"Error computing correlation for {row['filename_1']} and {row['filename_2']} with ROI {roi_name}: {e}")
                    correlations.append(np.nan)

        df_pairs[f'corr_{roi_name}'] = correlations
    return df_pairs


rois_dir = '/data/gpfs/projects/punim2239/data/rois_final'
working_dir = '/data/gpfs/projects/punim2239/data/rsa_pairs'
trial_dir = '/data/gpfs/projects/punim2239/data/first_zstat_4mm'
df_pairs = pd.read_csv(f'{working_dir}/all_file_pairs.csv')

roi_masks = {
    'win_lose': f'{rois_dir}/Win_vs_lose_group_bin.nii.gz',
    'amygdala': f'{rois_dir}/amy_z10_subjspace_bin.nii.gz',
    'insula': f'{rois_dir}/insula_z7_subjspace_bin.nii.gz',
    'antvmPFC': f'{rois_dir}/mask_6mm_antvmPFC_Qi.nii.gz',
    'vmpfc': f'{rois_dir}/vmpfc_neurovault_subjspace_bin.nii.gz',
}

# Get all unique filenames from the DataFrame
unique_files = pd.concat([df_pairs['filename_1'], df_pairs['filename_2']]).unique()
preprocessed_data = load_and_mask_data(unique_files, roi_masks, trial_dir)
df_pairs = compute_correlations(df_pairs, preprocessed_data, roi_masks)

# Save the updated DataFrame with correlations
df_pairs.to_csv(f'{working_dir}/all_pairs_corr_4mm_smooth.csv', index=False)
