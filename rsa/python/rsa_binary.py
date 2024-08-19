import nibabel as nib
import numpy as np
import pandas as pd
import glob
import re
import os
from scipy.stats import pearsonr, zscore

# for running on locally on test files:
# data_dir = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/matlab/data/test_files/'
# working_dir = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/repos/and_lab/'
# mask_4mm = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/matlab/data/new_rois/mask_4mm_antvmPFC_Qi.nii.gz'
# mask_6mm = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/matlab/data/new_rois/mask_6mm_antvmPFC_Qi.nii.gz'

data_dir = '/data/gpfs/projects/punim2239/data/first_zstat_6mm/'
working_dir = '/data/gpfs/projects/punim2239/scripts/python/'
mask_4mm = '/data/gpfs/projects/punim2239/data/new_rois/mask_4mm_antvmPFC_Qi.nii.gz'
mask_6mm = '/data/gpfs/projects/punim2239/data/new_rois/mask_6mm_antvmPFC_Qi.nii.gz'

masks = {'4mm': mask_4mm, '6mm': mask_6mm}

df_pairs = pd.read_csv(f'{working_dir}file_pairs.csv', index_col=None)
df_pairs = df_pairs[~df_pairs['subject'].isin(['7', 7])]
# filter df_pairs to the test files only
# df_pairs = df_pairs[(df_pairs['round1'].isin([1, 2]))&(df_pairs['round2'].isin([1, 2]))&(df_pairs['trial'].isin([1, 2]))]
files = list(df_pairs['file1'].unique()) # get unique left hand file names

#%% main pairwise correlation/ distance calculation
for mask_key in masks.keys():
    print(f'Started processing for mask: {mask_key}')
    mask = nib.load(masks[mask_key]).get_fdata()
    disimilarities = []
    for file1 in files:
        file1_failed = False
        print(f'Started processing for file 1: {file1}')
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

    df_pairs.to_csv(f'{working_dir}file_pairs_{mask_key}.csv')

#%% group by pairings to get RDM
# df_gby = df_pairs.groupby(['stim1', 'stim2'])['disim'].mean().reset_index()
# rdm = df_gby.pivot(index='stim1', columns='stim2', values='disim')
# columns = rdm.columns
# index = rdm.index
# rdm =rdm.values
# rdm = np.triu(rdm) + np.triu(rdm, 1).T
# df_rdm = pd.DataFrame(rdm, columns=columns, index=index)
# order = ['cat', 'goose', 'lion', 'grizzly', 'fist', 'stick', 'gun', 'grenade']
# df_rdm = df_rdm.loc[order, order]
