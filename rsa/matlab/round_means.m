% This function works out the mean activation per round to use for demeaning. 
% 

function mean_activation = round_means(stim_path, roi_path, subids, stim, masks, rounds, trials_lookup)

mean_activation = cell(length(subids), length(masks), length(rounds));

for mask_idx = 1:length(masks)
    mask_name = masks{mask_idx}; % Iterate through each ROI
    for sub = 1:length(subids)
        for r = 1:length(rounds)
            current_round_samples = [];
            for a = 1:length(stim) % Loop through animals/weapons
                % Determine the number of trials for the current condition
                trial_key = sprintf('R%s_%s', rounds{r}, stim{a}); % Construct the key for lookup
                num_trials = trials_lookup.(trial_key); % Get the number of trials from the lookup table
                for t = 1:num_trials
                    % Construct file name and load dataset
                    file_name = sprintf('%s_sub%s_%s%d.nii.gz', trial_key, subids{sub}, stim{a}, t);
                    file_path = fullfile(stim_path, file_name);
                    if isfile(file_path)
                        try
                            ds_trial = cosmo_fmri_dataset(file_path, 'mask', fullfile(roi_path, mask_name));
                            current_round_samples(:, end+1) = ds_trial.samples'; % Append samples to current round
                        catch ME
                            fprintf('Error loading file: %s\nError message: %s\n', file_name, ME.message);
                        end
                    else
                        fprintf('File not found: %s\n', file_name);
                    end
                end
            end
            if ~isempty(current_round_samples)
                round_mean = mean(current_round_samples, 2); % Mean across columns (samples)
            end 
            mean_activation{sub, mask_idx, r} = round_mean;
            fprintf('Added mean activation for mask %s, subject %s, round %s\n', mask_name, subids{sub}, rounds{r});

        end
    end
end
    