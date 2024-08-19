import nibabel as nib

trial_file_path = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/matlab/data/test_files/R1_cat_sub3_cat1.nii.gz'
mask_file_path = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/matlab/data/ROI_subject/sub01_antvmPFC.nii.gz'

trial_file = nib.load(trial_file_path)
mask_file = nib.load(mask_file_path)
image_data = trial_file.get_fdata()
header = trial_file.header

print("Data shape:", image_data.shape)
print("Data type:", image_data.dtype)
print("Header info:", header)
