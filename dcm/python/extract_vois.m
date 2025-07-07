%% Description
% This function runs VOI extraction for one contrast, the general TASK
% contrast. It loops through all participants.

function extract_vois(subject_id, version, task_num, condition)

%% SET UP
spm('Defaults','fMRI');
spm_jobman('initcfg');
spm_get_defaults('cmdline', true);

% Set parameters
contrast_num = 2; % use task contrast to extract VOIs
p_threshold = 0.05; % p-value threshold

% Define filepaths and names

task_num_str = num2str(task_num);

fear_task = ['fear_', task_num_str];
folder = [fear_task, '_', condition];

masks_dir = '/data/gpfs/projects/punim2239/dcm/data/masks';
output_dir     = fullfile('/data/gpfs/projects/punim2239/panda/data/output', version, folder);
masks = struct( ... 
    'antvmpfc', fullfile(masks_dir, 'antvmpfc_bin_clean.nii'), ...
    'postvmpfc', fullfile(masks_dir, 'postvmpfc_bin_clean.nii'), ...
    'amygdala', fullfile(masks_dir, 'amygdala_bin_clean.nii'), ...
    'striatum', fullfile(masks_dir, 'striatum_bin_clean.nii'), ...
    'lpsts', fullfile(masks_dir, 'lpsts_bin_clean.nii'), ...
    'hipp', fullfile(masks_dir, 'hipp_bin_clean.nii') ...
);
roi_names = fieldnames(masks);

%% MAIN LOOP
disp(['Processing subject ', num2str(subject_id), '...']);
if subject_id == 1000
    subject_id_str = '1000';
else
    subject_id_str = sprintf('%03d', subject_id);
end
spm_dir = fullfile(output_dir, subject_id_str); % define spm directory for subject

clear matlabbatch

for r = 1:length(roi_names) % Loop over ROIs
    matlabbatch{r}.spm.util.voi.spmmat(1) = {fullfile(spm_dir, 'SPM.mat')};
    matlabbatch{r}.spm.util.voi.adjust = 1; % Adjust data for [effects of interest], enter index for F-contrast created above; 0 for no adjustment; NaN adjust for everything
    matlabbatch{r}.spm.util.voi.session = 1;
    matlabbatch{r}.spm.util.voi.name = [roi_names{r}, '_' ,subject_id_str];
    matlabbatch{r}.spm.util.voi.roi{1}.spm.spmmat = {''};
    matlabbatch{r}.spm.util.voi.roi{1}.spm.contrast = contrast_num; % 1=EoF, 2=Task,
    matlabbatch{r}.spm.util.voi.roi{1}.spm.conjunction = 1;
    matlabbatch{r}.spm.util.voi.roi{1}.spm.threshdesc = 'none';
    matlabbatch{r}.spm.util.voi.roi{1}.spm.thresh = p_threshold; %convention is .05 (end of Ziedmann 2019 p1)
    matlabbatch{r}.spm.util.voi.roi{1}.spm.extent = 0; %common to use 0, deciding on the number of voxels to classify as VOI
    matlabbatch{r}.spm.util.voi.roi{1}.spm.mask = struct('contrast', {}, 'thresh', {}, 'mtype', {});
    matlabbatch{r}.spm.util.voi.roi{2}.mask.image = {fullfile(masks_dir, [roi_names{r}, '_bin_clean.nii'])};
    matlabbatch{r}.spm.util.voi.roi{2}.mask.threshold = 0.5;
    matlabbatch{r}.spm.util.voi.expression = 'i1 & i2'; %extract masked region (pt2) from thresholded VOI (pt1)
end

spm_jobman('run', matlabbatch); % Run the VOI extraction

%% --- COUNT VOXELS: write straight to stdout -----------------------------
for r = 1:numel(roi_names)
    voi_nii = fullfile(spm_dir, ['VOI_%s_%s_1.nii',roi_names{r}, subject_id_str]);
    if exist(voi_nii,'file')
        nvox = nnz(spm_read_vols(spm_vol(voi_nii)));
        fprintf('Subject %s  ROI %-10s : %d voxels in final mask\n', ...
                subject_id_str, roi_names{r}, nvox);
    else
        fprintf(2, 'WARNING: VOI file %s not found – skipping voxel count\n', voi_nii);
    end
end