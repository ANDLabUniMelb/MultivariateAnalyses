function first_level_dcm(subject_id, version, task_num, condition)

%% SET UP
spm('Defaults','fMRI');
spm_jobman('initcfg');
spm_get_defaults('cmdline', true);

% Parameters
task_num_str = num2str(task_num);
TR          = 3;
hpf_cutoff  = 128;

fear_task = ['fear_', task_num_str];
folder = [fear_task, '_', condition];
conditions = {'Task', ...
    ['CS+', condition], ['CS-', condition], ...
    'Fixation', 'Question', 'Scream', ...
    };

if subject_id == 1000
    subject_id_str = '1000';
else
    subject_id_str = sprintf('%03d', subject_id);
end

sub_dir    = fullfile('/data/gpfs/projects/punim2239/panda/panda_fmri_prep', ...
                       ['sub-EA' subject_id_str],'func');
output_dir     = fullfile('/data/gpfs/projects/punim2239/panda/data/output', version, folder);
sub_output_dir = fullfile(output_dir, subject_id_str);

%% 1) CREATE BATCH AND DIRECTORIES

clear matlabbatch;
matlabbatch{1}.cfg_basicio.file_dir.dir_ops.cfg_mkdir.parent = {output_dir};
matlabbatch{1}.cfg_basicio.file_dir.dir_ops.cfg_mkdir.name   = subject_id_str;

%% 2) SPECIFY

matlabbatch{2}.spm.stats.fmri_spec.dir            = {sub_output_dir};
matlabbatch{2}.spm.stats.fmri_spec.timing.units   = 'secs';
matlabbatch{2}.spm.stats.fmri_spec.timing.RT      = TR;
matlabbatch{2}.spm.stats.fmri_spec.timing.fmri_t  = 16;
matlabbatch{2}.spm.stats.fmri_spec.timing.fmri_t0 = 8;
matlabbatch{2}.spm.stats.fmri_spec.bases.hrf.derivs = [0 0];
matlabbatch{2}.spm.stats.fmri_spec.volt           = 1;
matlabbatch{2}.spm.stats.fmri_spec.global         = 'None';
matlabbatch{2}.spm.stats.fmri_spec.mthresh        = 0.01;
matlabbatch{2}.spm.stats.fmri_spec.mask           = {'/data/gpfs/projects/punim2239/dcm/data/masks/MNI152_T1_2mm_brain_mask_new_bin_clean.nii,1'};
matlabbatch{2}.spm.stats.fmri_spec.cvi            = 'FAST';

pattern  = ['^sub-EA' subject_id_str ...
            '_task-fear' task_num_str ...
            '_space-MNI152NLin2009cAsym_res-2_desc-preproc_bold\.nii$'];


files = spm_select('ExtFPList', sub_dir, pattern, Inf);

if isempty(files)
    error('Subject %s – task %s missing, aborting single‑session setup', ...
           subject_id_str, task_num_str);
end

% Populate the (single) session
matlabbatch{2}.spm.stats.fmri_spec.sess(1).scans     = cellstr(files);
matlabbatch{2}.spm.stats.fmri_spec.sess(1).multi     = {''};

confounds_file = fullfile(sub_dir, ...
    sprintf('sub-EA%s_task-fear%s_motion24.txt', ...
            subject_id_str, task_num_str));
M = readmatrix(confounds_file,'Delimiter','\t');  
M_filled = fillmissing(M, 'next');
writematrix(M_filled, confounds_file, 'Delimiter','tab');

matlabbatch{2}.spm.stats.fmri_spec.sess(1).multi_reg = {confounds_file};
matlabbatch{2}.spm.stats.fmri_spec.sess(1).regress   = struct('name',{},'val',{});
matlabbatch{2}.spm.stats.fmri_spec.sess(1).hpf       = hpf_cutoff;

onset_dir = fullfile('/data/gpfs/projects/punim2239/panda/onsets', ['fear' task_num_str '_onsets']);

for c = 1:numel(conditions)
    onsets = load(fullfile(onset_dir, [conditions{c},'.txt']));

    matlabbatch{2}.spm.stats.fmri_spec.sess(1).cond(c).name     = conditions{c};
    matlabbatch{2}.spm.stats.fmri_spec.sess(1).cond(c).onset    = onsets(:,1)';
    matlabbatch{2}.spm.stats.fmri_spec.sess(1).cond(c).duration = onsets(:,2)';

    % no parametric modulators:
    matlabbatch{2}.spm.stats.fmri_spec.sess(1).cond(c).pmod = struct('name',{},'param',{},'poly',{});
    matlabbatch{2}.spm.stats.fmri_spec.sess(1).cond(c).tmod = 0;
    matlabbatch{2}.spm.stats.fmri_spec.sess(1).cond(c).orth = 0;
end

%% 3) ESTIMATE

matlabbatch{3}.spm.stats.fmri_est.spmmat = { fullfile(sub_output_dir,'SPM.mat') };
matlabbatch{3}.spm.stats.fmri_est.method.Classical = 1;

%% 4) CONTRASTS

matlabbatch{4}.spm.stats.con.spmmat = {fullfile(sub_output_dir,'SPM.mat')};

idx_dcm = [1 2 3];

E = zeros(numel(idx_dcm), length(conditions));
for k = 1:numel(idx_dcm)
    E(k, idx_dcm(k)) = 1;
end

matlabbatch{4}.spm.stats.con.consess{1}.fcon.name    = 'Effects of interest';
matlabbatch{4}.spm.stats.con.consess{1}.fcon.weights = E;
matlabbatch{4}.spm.stats.con.consess{1}.fcon.sessrep = 'none';

matlabbatch{4}.spm.stats.con.consess{2}.tcon.name     = [conditions{idx_dcm(1)}]; 
matlabbatch{4}.spm.stats.con.consess{2}.tcon.weights = [1 0 0 zeros(1, 3)];
matlabbatch{4}.spm.stats.con.consess{2}.tcon.sessrep = 'none';
matlabbatch{4}.spm.stats.con.consess{3}.tcon.name     = [conditions{idx_dcm(2)}]; 
matlabbatch{4}.spm.stats.con.consess{3}.tcon.weights = [0 1 0 zeros(1, 3)];
matlabbatch{4}.spm.stats.con.consess{3}.tcon.sessrep = 'none';
matlabbatch{4}.spm.stats.con.consess{4}.tcon.name     = [conditions{idx_dcm(3)}]; 
matlabbatch{4}.spm.stats.con.consess{4}.tcon.weights = [0 0 1 zeros(1, 3)];
matlabbatch{4}.spm.stats.con.consess{4}.tcon.sessrep = 'none';

matlabbatch{4}.spm.stats.con.consess{5}.tcon.name     = [conditions{idx_dcm(2)} '>' conditions{idx_dcm(3)}]; 
matlabbatch{4}.spm.stats.con.consess{5}.tcon.weights = [0 1 -1 zeros(1, 3)];
matlabbatch{4}.spm.stats.con.consess{5}.tcon.sessrep = 'none';
matlabbatch{4}.spm.stats.con.consess{6}.tcon.name     = [conditions{idx_dcm(3)} '>' conditions{idx_dcm(2)}]; 
matlabbatch{4}.spm.stats.con.consess{6}.tcon.weights = [0 -1 1 zeros(1, 3)];
matlabbatch{4}.spm.stats.con.consess{6}.tcon.sessrep = 'none';

matlabbatch{4}.spm.stats.con.delete = 0;

%% RUN

spm_jobman('run', matlabbatch);
end