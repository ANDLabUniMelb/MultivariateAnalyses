# Script to create binarized version of ROI nii files
import os
import nibabel as nib
import numpy as np

input_folder = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/data/fsleyes'
output_folder = '/Users/joecussen/Documents/Jobs/unimelb/projects/dcm/data/fsleyes/binarized'
files = ['amygdala.nii', 'antvmpfc.nii', 'lpsts.nii', 'postvmpfc.nii', 'striatum.nii', 'MNI152_T1_2mm_brain_mask_new.nii']

os.makedirs(output_folder, exist_ok=True)  # Create the output directory if it doesn't exist

for file in files:
    input_path = os.path.join(input_folder, file)
    output_path = os.path.join(output_folder, file.replace('.nii', '_bin.nii'))

    # Load the NIfTI file
    nii = nib.load(input_path)
    data = nii.get_fdata()

    # Binarize: All non-zero values become 1
    bin_data = (data > 0).astype(np.uint8)

    # Save the binarized file
    bin_nii = nib.Nifti1Image(bin_data, affine=nii.affine, header=nii.header)
    nib.save(bin_nii, output_path)
