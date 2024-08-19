import nibabel as nib
import numpy as np
import pandas as pd
import glob
import re
import os
from scipy.stats import pearsonr, zscore

data_dir = '/data/gpfs/projects/punim2239/data/first_zstat_4mm/'
mask_dir = '/data/gpfs/projects/punim2239/data/ROI_subject/'
working_dir = '/data/gpfs/projects/punim2239/scripts/python/'

df_pairs = pd.read_csv(f'{working_dir}file_pairs.csv', index_col=None)
# filter df_pairs to the test files only
df_pairs = df_pairs[~df_pairs['subject'].isin(['7', 7])]
# df_pairs = df_pairs[(df_pairs['round1'].isin([1, 2]))&(df_pairs['round2'].isin([1, 2]))&(df_pairs['trial'].isin([1, 2]))]
files = list(df_pairs['file1'].unique()) # get unique left hand file names

 #%%

def get_subject_number(filename):
    ''' helper function to get subject number from filename '''
    pattern = re.compile(r'sub(\d+)_')
    match = pattern.search(filename)
    if match:
        return match.group(1)  # group(1) returns the first capturing group in the match
    else:
        return "Subject number not found"

def get_subject_masks(folder_path):
    ''' function to read in all subject masks data into dictionary '''
    pattern = re.compile(r'sub(\d+)_(\w+)\.nii\.gz')
    data_dict = {}
    file_paths = glob.glob(os.path.join(folder_path, '*.nii.gz'))

    for file_path in file_paths:
        filename = os.path.basename(file_path)
        match = pattern.match(filename)

        if match:
            subject_number = str(int(match.group(1)))
            roi_name = match.group(2)
            file_data = nib.load(file_path)
            if roi_name not in data_dict:
                data_dict[roi_name] = {}
            data_dict[roi_name][subject_number] = file_data

    return data_dict

mask_dict = get_subject_masks(mask_dir)

#%% main pairwise correlation/ distance calculation
rois = ['antvmPFC', 'postvmPFC', 'PAG', 'BilateralAmy_z10_6mm', 'BilateralInsula_z10_6mm']

for roi in rois:
    print(f'Started processing for ROI: {roi}')
    disimilarities = []
    for file1 in files:
        file1_failed = False
        print(f'Started processing for file 1: {file1}')
        subject= get_subject_number(file1)
        mask = mask_dict[roi][subject].get_fdata() # get mask data file
        try:
            data_img1 = nib.load(f'{data_dir}{file1}') # get first data file
            data1 = data_img1.get_fdata()[mask != 0] # apply roi mask
        except Exception as e:
            file1_failed = True
            print(f'Failed to process file1: {file1}')
            print(e)



        df_file = df_pairs[df_pairs['file1']==file1] # create filtered df
        for _, row in df_file.iterrows():
            if not file1_failed:
                file2 = row['file2'] # get second file name
                print(f'Started processing for file 2: {file2}')
                try:
                    data_img2 = nib.load(f'{data_dir}{file2}') # get second data file
                    data2 = data_img2.get_fdata()[mask != 0] # apply roi mask
                    correlation, _ = pearsonr(zscore(data1), zscore(data2)) # calc corr of zscore data
                    fisher_z = np.arctanh(correlation) # fisher transform
                    dist = 1- fisher_z # disim transform
                    disimilarities.append(dist)
                except Exception as e:
                    disimilarities.append(np.nan)
                    print(f'Failed to process file2: {file2}')
                    print(e)
            else:
                disimilarities.append(np.nan)

    df_pairs['disim'] = disimilarities

    df_pairs.to_csv(f'{working_dir}file_pairs_{roi}.csv')

# #%% group by pairings to get RDM
# df_gby = df_pairs.groupby(['stim1', 'stim2'])['disim'].mean().reset_index()
# rdm = df_gby.pivot(index='stim1', columns='stim2', values='disim')
# columns = rdm.columns
# index = rdm.index
# rdm =rdm.values
# rdm = np.triu(rdm) + np.triu(rdm, 1).T
# df_rdm = pd.DataFrame(rdm, columns=columns, index=index)
# order = ['cat', 'goose', 'lion', 'grizzly', 'fist', 'stick', 'gun', 'grenade']
# df_rdm = df_rdm.loc[order, order]
