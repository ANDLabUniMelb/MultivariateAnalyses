clc
clear

script_dir = fileparts(mfilename('fullpath'));
addpath latest_IC_toolbox/
addpath(genpath(fullfile(script_dir, 'CoSMoMVPA-master')));
addpath rois_new/

cond_cat = 'WEAPON';
roi_names = {'ACC', 'AMY', 'DLPFC_L', 'DLPFC_R', 'HC', 'PAG', 'T', 'antvmpfc_10mm_subjspace_bin', 'postvmpfc_10mm_subjspace_bin', 'HO_insula', 'striatum_1_subjspace_bin', 'striatum_2_subjspace_bin', 'striatum_3_subjspace_bin',};
results_dir = '/Users/joecussen/Documents/Jobs/unimelb/adaptive_safety_coding/data/IC/spartan/results_first_zstat_270524_weapons';

categories = {'all', 'simple'};

for i = 1:length(categories) % Loop through each category to initialise the matrices
    load(fullfile(results_dir,['ICMs_' cond_cat '_' categories{i} '.mat']));
    load(fullfile(results_dir,['pvalues_' cond_cat '_' categories{i} '.mat']));
    ICM_mean = squeeze(mean(ICMs_save, 1));
    plot_ICM(ICM_mean, roi_names, '', results_dir, ['mean_' categories{i}])
    stouffer_pvalues = stouffer_method(pvalues_save);
    binary_connection_matrix = stouffer_pvalues < 0.05;
    plot_ICM(binary_connection_matrix, roi_names, '', script_dir, ['binary_sig_' categories{i}])
    save(fullfile(results_dir, ['binary_matrix_' categories{i} '.mat']), 'binary_connection_matrix')
end
