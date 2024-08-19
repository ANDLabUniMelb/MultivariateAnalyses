clear;
clc;

run_condition = 'test'; % run_condition: 'first_zstat', 'second_zstat', 'test'
smooth = '6mm'; % smooth: '', '4mm', '6mm'

[stim_path, roi_path, fig_path, results_path, subids, stim, masks, rounds, trials_lookup, RDMs] = rsa_setup(run_condition, smooth);

for mask_idx = 1:length(masks)
    mask_name = masks{mask_idx}; % Iterate through each ROI
    fprintf('\nProcessing mask: %s\n', mask_name);

    for sub = 1:length(subids)
        fprintf('Processing Subject %s for ROI %s...\n', subids{sub}, mask_name);
        dat_all = []; % Initialize to store all data for this subject
        dat_stim = []; % Temporarily store data for each stim
        count_stim = []; % Count total trials per condition 
        for a = 1:length(stim) % Loop through animals/weapons
            counter = 0;
            for r = 1:length(rounds)
                % Determine the number of trials for the current condition
                trial_key = sprintf('R%s_%s', rounds{r}, stim{a}); % Construct the key for lookup
                num_trials = trials_lookup.(trial_key); % Get the number of trials from the lookup table
                disp(['The number of trials is: ', num2str(num_trials)])
                for t = 1:num_trials
                    % Construct file name and load dataset
                    file_name = sprintf('%s_sub%s_%s%d.nii.gz', trial_key, subids{sub}, stim{a}, t);
                    file_path = fullfile(stim_path, file_name);
                    if isfile(file_path)
                        try
                            ds_trial = cosmo_fmri_dataset(file_path, 'mask', fullfile(roi_path, mask_name));
                            dat_stim(:, end+1) = ds_trial.samples'; % Append samples to dat_stim
                            counter = counter + 1;
                        catch ME
                            fprintf('Error loading file: %s\nError message: %s\n', file_name, ME.message);
                        end
                    else
                        fprintf('File not found: %s\n', file_name);
                    end
                end
            end

            count_stim(:, end+1) = counter;

        end

        dat_filt = dat_stim(any(dat_stim,2), :); % Filter out rows with all zeros
        z_all = zscore(dat_filt, 0, 1); % Z-score normalization
        sim_mat = corr(z_all, 'Type', 'Pearson'); % Compute correlation matrix

        stim_idx = cumsum(count_stim);
        % Pre-compute start and end indices for rows and columns
        row_starts = [1, stim_idx(1:end-1) + 1];
        col_starts = row_starts;  % Same as row_starts in this case
        row_ends = stim_idx;
        col_ends = row_ends;

        % Initialize matrix to store the mean values
        mean_mat = zeros(length(stim_idx));

        % Compute the mean for each submatrix, excluding diagonal when i = j
        for i = 1:length(row_starts)
            for j = 1:length(col_starts)
                sub_matrix = sim_mat(row_starts(i):row_ends(i), col_starts(j):col_ends(j));
                if i == j  % When i equals j, exclude the diagonal from the mean calculation
                    sub_matrix(logical(eye(size(sub_matrix)))) = NaN;  % Replace diagonal elements with NaN
                    mean_mat(i, j) = mean(sub_matrix(:), 'omitnan');  % Compute mean excluding NaN
                else
                    mean_mat(i, j) = mean(sub_matrix(:));  % Compute mean normally when i does not equal j
                end
            end
        end


        dissimilarity_mat = 1 - mean_mat;
        % dissimilarities_flat = dissimilarity_mat(tril(true(size(dissimilarity_mat)), -1));
        % percentiles_flat = arrayfun(@(x) mean(dissimilarities_flat < x), dissimilarities_flat) * 100;
        % percentile_mat = zeros(size(dissimilarity_mat)); % Initialize percentile matrix
        % percentile_mat(tril(true(size(percentile_mat)), -1)) = percentiles_flat;
        % percentile_mat = percentile_mat + percentile_mat';

        % % Diagonal elements represent self-similarity, should be 0
        % diag_idx = 1:size(dissimilarity_mat, 1) + 1:numel(dissimilarity_mat);
        % percentile_mat(diag_idx) = 0;

        % Store the percentile matrix in RDMs
        RDMs(:, :, sub, mask_idx) = mean_mat;
    end

    % Average RDM across all subjects for this ROI
    avg_RDM = mean(RDMs(:, :, :, mask_idx), 3);

    % Plotting the average RDM for each ROI
    fprintf('Plotting RDM for ROI: %s...\n', mask_name);
    figure; % Creates a new figure window
    imagesc(avg_RDM, [0, 1]); % Plots the RDM with scale set from 0 to 1 for clarity
    title(sprintf('%s - Average RDM', mask_name)); % Adds a title with the ROI name
    xlabel('Conditions'); % Labels the x-axis
    ylabel('Conditions'); % Labels the y-axis
    colorbar; % Adds a colorbar
    colormap('hot'); % Sets the colormap

    % Overlay numerical values
    [numRows, numCols] = size(avg_RDM);
    for row = 1:numRows
        for col = 1:numCols
            text(col, row, sprintf('%.2f', avg_RDM(row, col)), ...
                'HorizontalAlignment', 'center', ...
                'VerticalAlignment', 'middle');
        end
    end

    % Enhancing the plot
    axis square; % Makes the plot square in shape
    set(gca, 'TickLength', [0 0]); % Removes the ticks
    set(gca, 'XTick', 1:length(stim), 'XTickLabel', stim, 'YTick', 1:length(stim), 'YTickLabel', stim);
    xtickangle(45); % Tilts the x-axis labels for better readability

    % Save the figure
    fig_name = sprintf('%s_RDM.png', mask_name); % Define the figure name
    full_fig_path = fullfile(fig_path, fig_name); % Full path for the figure
    exportgraphics(gca, full_fig_path, 'Resolution', 300); % For higher quality (MATLAB R2020a and newer)
end

% Define the full path for the RDMs.mat file
rdms_file_path = fullfile(results_path, 'RDMs.mat');
save(rdms_file_path, 'RDMs');