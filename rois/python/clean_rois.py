# script to clean up ROI files by handling overlapping voxels and out of mask voxels
import os
import nibabel as nib
import numpy as np

input_folder = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/data/fsleyes/binarized'
output_folder = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/data/fsleyes/cleaned'
os.makedirs(output_folder, exist_ok=True)

files = [
    'amygdala_bin.nii', 'antvmpfc_bin.nii', 'lpsts_bin.nii',
    'postvmpfc_bin.nii', 'striatum_bin.nii',
]
mask_file = 'MNI152_T1_2mm_brain_mask_new_bin.nii'

roi_names = [os.path.splitext(file)[0] for file in files]
mask = nib.load(os.path.join(input_folder, mask_file)).get_fdata() > 0
rois = [nib.load(os.path.join(input_folder, file)) for file in files]
roi_data = [roi.get_fdata() > 0 for roi in rois]

# Check and resolve overlapping voxels
overlap_matrix = np.stack(roi_data, axis=-1)
voxel_sums = np.sum(overlap_matrix, axis=-1)
overlapping_voxels = np.where(voxel_sums > 1)

for idx in zip(*overlapping_voxels):
    overlapping_indices = [i for i, overlap in enumerate(overlap_matrix[idx]) if overlap]
    sizes = [np.sum(roi_data[i]) for i in overlapping_indices]
    largest_roi_index = overlapping_indices[np.argmax(sizes)]
    for i in overlapping_indices:
        if i != largest_roi_index:
            roi_data[i][idx] = False

# Check and remove voxels outside the mask
for i, roi in enumerate(roi_data):
    roi_data[i] = roi & mask

# Save all cleaned ROIs
for roi_name, roi, roi_orig in zip(roi_names, roi_data, rois):
    cleaned_data = roi.astype(np.uint8)
    cleaned_img = nib.Nifti1Image(cleaned_data, affine=roi_orig.affine, header=roi_orig.header)
    cleaned_path = os.path.join(output_folder, f"{roi_name}_clean.nii")
    nib.save(cleaned_img, cleaned_path)