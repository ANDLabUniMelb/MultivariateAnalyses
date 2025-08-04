%% Description
% This function estimates/fits the DCMs for all participants.

function dcm_load_fit(version, task_num, condition, spec)
%% SET UP
spm('Defaults', 'fMRI');
spm_jobman('initcfg');
spm_get_defaults('cmdline', true);

task_num_str = num2str(task_num);
fear_task = ['fear_', task_num_str];
folder = [fear_task, '_', condition];

% Set file locations
output_dir     = fullfile('/data/gpfs/projects/punim2239/panda/data/output', version, folder);

subject_ids = [8,9,10,16,21,26,36,37,39,44,48,49,57,58,92,94,104,115,120,121,136,143,146,156,161,169,190,193,198,220,221,222,254,282,303,323,341,350,363,375,393,398,403,407,421,433,448,449,485,528,544,595,596,641,643,660,673,682,688,693,714,730,746,747,760,777,779,806,840,847,858,861,864,866,870,875,885,889,895,898,910,913,914,918,920,939,946,1000];
num_subjects = numel(subject_ids);

filelist = '';

%% LOAD DCMs
for i = 1:num_subjects
    subject_id = subject_ids(i);
    % define filepaths
    if subject_id == 1000
        subject_id_str = '1000';
    else
        subject_id_str = sprintf('%03d', subject_id);
    end
    sub_dir = fullfile(output_dir, subject_id_str);

    % Load each DCM (spm_dcm_load returns a 1×1 cell array)
    DCM_full = fullfile(sub_dir, ['DCM_', spec, '_', subject_id_str, '.mat']);
    cur_filelist = dir(DCM_full);
    filelist = [filelist,cur_filelist];
end

%% FIT DCMs
GCM = fullfile({filelist.folder}, {filelist.name})';
GCM = spm_dcm_load(GCM);
GCM = spm_dcm_fit(GCM);
save(fullfile(output_dir, ['GCM_', version, '_', folder, '_', spec, '.mat']), 'GCM', '-v7.3');

end