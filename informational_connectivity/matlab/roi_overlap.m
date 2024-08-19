clc
clear

%% Add CosmoMVPA toolbox
script_dir = fileparts(mfilename('fullpath'));
addpath latest_IC_toolbox/
addpath(genpath(fullfile(script_dir, 'CoSMoMVPA-master')));
addpath rois_all/
% 'BilateralAmy_z10_6mm.nii.gz', 'BilateralInsula_z10_6mm.nii.gz'
rois = {'ACC.nii.gz', 'AMY.nii.gz', 'antvmpfc_10mm_subjspace_bin.nii.gz', 'DLPFC_L.nii.gz', 'DLPFC_R.nii.gz', 'HC.nii.gz', 'HO-insula-thr50-subjspace-bin.nii.gz', 'PAG.nii.gz', 'postvmpfc_10mm_subjspace_bin.nii.gz', 'striatum_1_subjspace_bin.nii.gz', 'striatum_2_subjspace_bin.nii.gz', 'striatum_3_subjspace_bin.nii.gz', 'T.nii.gz', 'VMPFC.nii.gz'};
roi_names = {'ACC', 'AMY', 'antvmpfc_10mm_subjspace_bin', 'DLPFC_L', 'DLPFC_R', 'HC', 'HO', 'PAG', 'postvmpfc_10mm_subjspace_bin', 'striatum_1_subjspace_bin', 'striatum_2_subjspace_bin', 'striatum_3_subjspace_bin', 'T', 'VMPFC'};

%% Read in and combine ROIs into one mask:
first_roi = cosmo_fmri_dataset(rois{1}, 'mask', []);
first_roi_samples = first_roi.samples(:);
num_voxels = numel(first_roi_samples);
overlap_matrix = zeros(num_voxels, length(rois)); % Initialize overlap matrix

for i = 1:length(rois) % Loop through each ROI and assign unique integers
    current_mask = cosmo_fmri_dataset(rois{i}, 'mask', []); % Load ROI as a dataset
    current_mask_samples = current_mask.samples(:); % Flatten the samples to a column vector
    
    % Ensure current_mask_samples has the same number of voxels as first_roi_samples
    if numel(current_mask_samples) ~= num_voxels
        error('Mismatch in number of voxels between %s and %s.', rois{1}, rois{i});
    end
    
    overlap_matrix(:, i) = current_mask_samples > 0; % Store binary mask in the overlap matrix
end

% Find voxels with overlapping ROIs
overlapping_voxels = find(sum(overlap_matrix, 2) > 1);

% Create a map to store counts of overlapping ROI names
unique_combinations = containers.Map('KeyType', 'char', 'ValueType', 'int32');

for j = 1:length(overlapping_voxels)
    voxel_idx = overlapping_voxels(j);
    overlapping_rois = find(overlap_matrix(voxel_idx, :));
    unique_rois = roi_names(overlapping_rois); % Get unique ROI names
    rois_str = strjoin(unique_rois, ', ');
    
    if isKey(unique_combinations, rois_str)
        unique_combinations(rois_str) = unique_combinations(rois_str) + 1;
    else
        unique_combinations(rois_str) = 1;
    end
end

% Display the results
unique_keys = keys(unique_combinations);
for k = 1:length(unique_keys)
    rois_str = unique_keys{k};
    count = unique_combinations(rois_str);
    fprintf('%d voxels overlap in ROIs: %s\n', count, rois_str);
end