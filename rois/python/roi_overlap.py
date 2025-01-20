# script to check ROI files don't overlap and are within mask file
import os
import nibabel as nib
import numpy as np
from collections import Counter

input_folder = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/data/fsleyes/binarized'
files = [
    'amygdala_bin.nii', 'antvmpfc_bin.nii', 'lpsts_bin.nii',
    'postvmpfc_bin.nii', 'striatum_bin.nii',
]
mask_file = 'MNI152_T1_2mm_brain_mask_new_bin.nii'

roi_names = [os.path.splitext(file)[0] for file in files]
mask = nib.load(os.path.join(input_folder, mask_file)).get_fdata() > 0
rois = [nib.load(os.path.join(input_folder, file)).get_fdata() > 0 for file in files]

overlap_matrix = np.stack(rois, axis=-1)
overlapping_voxels = np.where(np.sum(overlap_matrix, axis=-1) > 1)
overlap_details = []
for idx in zip(*overlapping_voxels):
    overlapping_rois = [roi_names[i] for i, overlap in enumerate(overlap_matrix[idx]) if overlap]
    overlap_details.append(tuple(sorted(overlapping_rois)))

overlap_counts = Counter(overlap_details)
for combination, count in overlap_counts.items():
    print(f'{count} voxels overlap in ROIs: {", ".join(combination)}')

for roi_name, roi_data in zip(roi_names, rois):
    outside_mask = np.sum(roi_data & ~mask)
    if outside_mask>0:
        print(f'{roi_name} has {outside_mask} voxels outside the mask')