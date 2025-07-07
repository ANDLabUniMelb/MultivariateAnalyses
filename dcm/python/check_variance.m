addpath('/Users/joecussen/Documents/Jobs/unimelb/repos/spm-main');

% Initialize SPM
spm('Defaults', 'fMRI');
spm_jobman('initcfg');
clear

load('GCM_0605_unsmooth_fear_1__earlyextinction_full_2.mat')

spm_dcm_fmri_check(GCM);