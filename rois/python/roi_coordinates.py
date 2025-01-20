# script to get the centre of ROI files

import os
import nibabel as nib
import numpy as np
from scipy.ndimage import label, distance_transform_edt

input_folder = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/data/fsleyes/cleaned'
files = [
    'amygdala_bin_clean.nii', 'antvmpfc_bin_clean.nii',
    'postvmpfc_bin_clean.nii', 'striatum_bin_clean.nii',
    'lpsts_bin_clean.nii',
]

for file in files:
    input_path = os.path.join(input_folder, file)
    img = nib.load(input_path)
    data = img.get_fdata() > 0

    # Label connected components and find the largest
    labeled, n_labels = label(data)
    largest_label = np.argmax([np.sum(labeled == i + 1) for i in range(n_labels)]) + 1
    largest_component = (labeled == largest_label)

    # Compute distance transform in mm (voxel size from affine diagonal if orthogonal)
    voxel_size = np.sqrt((img.affine[:3, :3] ** 2).sum(axis=0))
    distances = distance_transform_edt(largest_component, sampling=voxel_size)

    # Find voxel coordinate of maximum distance (largest inscribed sphere centre)
    max_idx = np.unravel_index(np.argmax(distances), distances.shape)
    centre_voxel = np.array(max_idx)
    centre_mm = nib.affines.apply_affine(img.affine, centre_voxel)
    distance_mm = distances[max_idx]

    print(file)
    print(f'Centroid (mm): {centre_mm}')
    print(f'Distance from centroid to edge (mm): {distance_mm:.2f}')
    print('\n')