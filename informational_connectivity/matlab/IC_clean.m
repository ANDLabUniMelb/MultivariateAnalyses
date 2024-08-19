clc
clear

%% Add CosmoMVPA toolbox
script_dir = fileparts(mfilename('fullpath'));
addpath latest_IC_toolbox/
addpath(genpath(fullfile(script_dir, 'CoSMoMVPA-master')));
addpath rois_all/

%% Define variables
name = 'rois1_clean'; % specific name for run e.g. roi group 1
run_condition = 'first_zstat'; % run_condition: 'first_zstat', 'second_zstat', 'test'
[stim_path, fig_path, results_path, subids, conditions, rounds, trials_lookup, lookup_table] = IC_setup(name, run_condition);

% ROI set 1:
rois = {'ACC_caudodorsal_bin_subjspace.nii.gz', 'ACC_pregenual_bin_subjspace.nii.gz', 'AMY.nii.gz', 'anterior_insula_bin_subjspace.nii.gz', 'antvmpfc_10mm_subjspace_bin.nii.gz', 'HC.nii.gz', 'PAG.nii.gz', 'postvmpfc_10mm_subjspace_bin.nii.gz', 'striatum_1_subjspace_bin.nii.gz', 'striatum_3_subjspace_bin.nii.gz', 'T.nii.gz',};
roi_names = {'ACC_caudodorsal', 'ACC_pregenual', 'AMY', 'anterior_insula', 'antvmpfc_10mm', 'HC', 'PAG', 'postvmpfc_10mm', 'striatum_1', 'striatum_3', 'T', };

% ROI set 2:
% rois = {'ACC_caudodorsal_bin_subjspace.nii.gz', 'ACC_pregenual_bin_subjspace.nii.gz', 'AMY.nii.gz', 'anterior_insula_bin_subjspace.nii.gz', 'HO_antvmpfc_bin_subjspace.nii.gz', 'HC.nii.gz', 'PAG.nii.gz', 'HO_postvmpfc_bin_subjspace.nii.gz', 'striatum_1_subjspace_bin.nii.gz', 'striatum_3_subjspace_bin.nii.gz', 'T.nii.gz',};
% roi_names = {'ACC_caudodorsal', 'ACC_pregenual', 'AMY', 'anterior_insula', 'HO_antvmpfc', 'HC', 'PAG', 'HO_postvmpfc', 'striatum_1', 'striatum_3', 'T', };


%% Read in and combine ROIs into one mask:
incremental_union_mask = zeros(size(cosmo_fmri_dataset(rois{1}, 'mask', []).samples)); % Initialize the union mask to zero

for i = 1:length(rois) % Loop through each ROI and assign unique integers
    current_mask = cosmo_fmri_dataset(rois{i}, 'mask', []); % Load ROI as a dataset
    incremental_union_mask(current_mask.samples > 0) = i; % Increment integers in the union mask
end
binary_union_mask = incremental_union_mask > 0; % Create a binary version of the union mask

%% Set up
categories = {'all', 'simple', 'animal', 'danger'}; % Define the categories
ICMs = cell(1, length(categories)); % Set up informational connectivity matrices
pvalues = cell(1, length(categories)); % Set up p value matrices

for i = 1:length(categories) % Loop through each category to initialise the matrices
    ICMs{i} = zeros(length(subids), length(rois), length(rois));
    pvalues{i} = zeros(length(subids), length(rois), length(rois));
end

%% Main loop
for sub_idx = 1:length(subids) % loop through subjects
    disp(['Processing Subject ', subids{sub_idx}]);
    ICs = cell(1, length(categories));
    for i = 1:length(categories) % set up each IC structure for each category
        ICs{i} = struct(); 
        ICs{i}.ROIs = incremental_union_mask(incremental_union_mask > 0)';
        ICs{i}.data = [];
        ICs{i}.conditions = [];
        ICs{i}.folds = [];
        ICs{i}.folds_conditions = {};
    end
    folds_data = {};
    folds_folds = {};
    min_fold = inf;
    for round_idx = 1:length(rounds) % Loop through rounds/folds
        for i = 1:length(categories) 
            ICs{i}.round_conditions = [];
        end
        round_samples = [];
        round_folds = [];
        
        for cond_idx = 1:length(conditions) % Loop through animals/weapons
            % Determine the number of trials for the current condition
            trial_key = sprintf('R%s_%s', rounds{round_idx}, conditions{cond_idx}); % Construct the key for lookup
            num_trials = trials_lookup.(trial_key); % Get the number of trials from the lookup table
            disp(['The number of trials is: ', num2str(num_trials)])
            for t = 1:num_trials
                % Construct file name and load dataset
                file_name = sprintf('%s_sub%s_%s%d.nii.gz', trial_key, subids{sub_idx}, conditions{cond_idx}, t);
                file_path = fullfile(stim_path, file_name);
                if isfile(file_path) % Check if file exists
                    try % Put in try block to catch errors
                        ds_trial = cosmo_fmri_dataset(file_path);
                        masked_samples = ds_trial.samples(binary_union_mask);
                        if any(masked_samples(:))
                            fprintf('Number of zero entries in masked_samples: %d\n', sum((masked_samples == 0), 'all'));
                            ICs{1}.round_conditions = [ICs{1}.round_conditions, full(sparse(cond_idx, 1, 1, length(conditions), 1))]; % All 8 conditions
                            ICs{2}.round_conditions = [ICs{2}.round_conditions, full(sparse(ceil(cond_idx/2), 1, 1, length(conditions)/2, 1))]; % 4 categories (safe animal, dangerous animal, weak weapon, strong weapon)
                            ICs{3}.round_conditions = [ICs{3}.round_conditions, full(sparse(ceil(cond_idx / 4), 1, 1, length(conditions)/4, 1))]; % 2 categories (animal, weapon)
                            ICs{4}.round_conditions = [ICs{4}.round_conditions, full(sparse(1 + mod(floor((cond_idx - 1) / 2), 2), 1, 1, length(conditions)/4, 1))]; % 2 categories (safe, dangerous)
                            round_samples = [round_samples, masked_samples']; 
                            round_folds = [round_folds, round_idx];
                        else 
                            disp('All entries are zero for this trial');
                        end
                    catch ME % Handle errors
                        disp(['Error loading file: ', file_path])
                        disp(['Error message: ', ME.message]);
                    end
                else
                    disp(['File not found: ', file_path]);
                end
            end    
        end
        for i = 1:length(categories) % add round data to fold data
            ICs{i}.folds_conditions{round_idx} = ICs{i}.round_conditions;
        end
        folds_data{round_idx} = round_samples;
        folds_folds{round_idx} = round_folds;
        if size(round_samples, 2) < min_fold 
            min_fold = size(round_samples, 2); % update minimum fold size
        end
    end
    
    for round_idx = 1:length(rounds) % select the same amount of samples per fold
        round_samples_z = nanzscore(folds_data{round_idx});
        for i = 1:length(categories) % add zscored trial values to data
            ICs{i}.data = [ICs{i}.data, round_samples_z(:, 1:min_fold)];
            ICs{i}.conditions = [ICs{i}.conditions, ICs{i}.folds_conditions{round_idx}(:, 1:min_fold)];
            ICs{i}.folds = [ICs{i}.folds, folds_folds{round_idx}(:, 1:min_fold)];
        end
    end
    
    rows_to_remove = all(ICs{1}.data == 0, 2); % remove any voxels that are always null for this subject
    b_removed = ICs{1}.ROIs(rows_to_remove, :);
    disp(['Rows removing:', num2str(length(b_removed))]);
    disp('ROIs containing zero values:');
    disp(unique(b_removed));
    for i = 1:length(categories) % remove rows and set selector and ROI names
        ICs{i}.data(rows_to_remove, :) = [];
        ICs{i}.ROIs(rows_to_remove, :) = [];
        ICs{i}.selector = ones(1, length(ICs{i}.folds));
        ICs{i}.ROI_names = roi_names;
    end

    % print the size of all inputs
    disp(['Size of IC{1}.data: ', num2str(size(ICs{1}.data))]);
    disp(['Size of IC{1}.conditions: ', num2str(size(ICs{1}.conditions))]);
    disp(['Size of IC{1}.folds: ', num2str(size(ICs{1}.folds))]);
    disp(['Size of IC{1}.ROIs: ', num2str(size(ICs{1}.ROIs))]);
    disp(['Size of IC{1}.ROI_names: ', num2str(size(ICs{1}.ROI_names))]);
    disp(['Size of IC{1}.selector: ', num2str(size(ICs{1}.selector))]);

    for i = 1:length(categories) % run IC analyis for each category
        [ICs{i}, ICM] = run_ROI_IC(ICs{i});
        [ICs{i}, pvalue] = permute_ROI_IC(ICs{i}, 1);
        ICMs{i}(sub_idx, :, :) = ICM;
        pvalues{i}(sub_idx, :, :) = pvalue;
        plot_ICM(ICM, roi_names, subids{sub_idx}, fig_path, categories{i})
    end
end

%% Save results, check significance and plot
for i = 1:length(categories) % aggregate and plot categories
    ICM_mean = squeeze(mean(ICMs{i}, 1));
    ICMs_save = ICMs{i};
    pvalues_save = pvalues{i};
    stouffer_pvalues = stouffer_method(pvalues_save);
    binary_connection_matrix = stouffer_pvalues < 0.05;
    plot_ICM(binary_connection_matrix, roi_names, '', fig_path, ['binary_sig_' categories{i}])
    plot_ICM(ICM_mean, roi_names, '', fig_path, ['mean_' categories{i}])
    save(fullfile(results_path, ['ICMs_' categories{i} '.mat']), 'ICMs_save');
    save(fullfile(results_path, ['pvalues_' categories{i} '.mat']), 'pvalues_save');
    save(fullfile(results_path, ['binary_matrix_' categories{i} '.mat']), 'binary_connection_matrix')
end