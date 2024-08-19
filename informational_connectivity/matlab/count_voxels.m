% Add the path to the CoSMoMVPA toolbox if needed
script_dir = fileparts(mfilename('fullpath'));
addpath(genpath(fullfile(script_dir, 'CoSMoMVPA-master')));
addpath rois/
addpath rois_sarah/

% List of ROI files
rois = {'ACC.nii.gz', 'AMY.nii.gz', 'BilateralAmy_z10_6mm.nii.gz', 'BilateralInsula_z10_6mm.nii.gz', 'DLPFC_L.nii.gz', 'DLPFC_R.nii.gz', 'HC.nii.gz', 'PAG.nii.gz', 'T.nii.gz', 'VMPFC.nii.gz'};
rois_2 = {'antvmpfc_10mm_subjspace_bin.nii.gz', 'HO-insula-thr50-subjspace-bin.nii.gz', 'postvmpfc_10mm_subjspace_bin.nii.gz', 'striatum_1_subjspace_bin.nii.gz', 'striatum_2_subjspace_bin.nii.gz', 'striatum_3_subjspace_bin.nii.gz', 'striatum_subjspace_bin.nii.gz'};

% Loop through each ROI file
for i = 1:length(rois)
    % Load the NIfTI file using cosmo_fmri_dataset
    roi_file = rois{i};
    ds = cosmo_fmri_dataset(roi_file);
    
    % Get the data from the dataset
    data = ds.samples;
    
    % Count the number of non-zero voxels
    num_voxels = nnz(data);
    num_ones = sum(data(:) == 1);
    
    % Print the number of voxels
    fprintf('Number of voxels in %s: %d\n', roi_file, num_voxels);
end