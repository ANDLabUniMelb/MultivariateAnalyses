script_dir = fileparts(mfilename('fullpath'));
addpath(fullfile(script_dir, 'spm-main'));  % Ensure SPM functions are added to the path
addpath decoding_toolbox/
addpath libsvm/matlab/
mask_path = fullfile(script_dir, 'GM_newspace_bin.nii');
data_dir = '/data/gpfs/projects/punim2239/data/second_zstat_unzipped/';
results_path = fullfile(script_dir, 'results');

% Check if the directory does not exist
if ~exist(results_path, 'dir')
    mkdir(results_path); % Create the directory
end

% Read the data table
data = readtable('direction_lookup_full.csv');

% Verify field names in data table
expected_fields = {'filename', 'chunk', 'label', 'stim'};
if ~all(ismember(expected_fields, data.Properties.VariableNames))
    error('The input data table must contain the columns: %s', strjoin(expected_fields, ', '));
end

% Set defaults
cfg = decoding_defaults;
cfg.results.overwrite = 1;
cfg.results.dir = results_path;

% Set the analysis that should be performed (default is 'searchlight')
cfg.analysis = 'wholebrain'; % standard alternatives: 'wholebrain', 'ROI' (pass ROIs in cfg.files.mask, see below)
cfg.searchlight.radius = 12; % use searchlight of radius 3 (by default in voxels), see more details below

% Set the filename of your brain mask (or your ROI masks as cell array)
cfg.files.mask = mask_path;

x = dir([data_dir, '*.nii']);
y = {x.name};

% Create a table from the list of filenames
fileTable = table(y', 'VariableNames', {'filename'});

% Perform the join operation
resultTable = innerjoin(data, fileTable, 'Keys', 'filename');

% Enable scaling min0max1 (otherwise libsvm can get VERY slow)
cfg.scale.method = 'min0max1';
cfg.scale.estimation = 'all'; % scaling across all data is equivalent to no scaling (i.e. will yield the same results), it only changes the data range which allows libsvm to compute faster

% Decide whether you want to see the searchlight/ROI/... during decoding
cfg.plot_selected_voxels = 0; % 0: no plotting, 1: every step, 2: every second step, 100: every hundredth step...

% Add additional output measures if you like
cfg.results.output = {'accuracy', 'confusion_matrix'};

% Define subsets
all_stim = {'cat', 'goose', 'lion', 'grizzly', 'fist', 'stick', 'gun', 'grenade'};
animals = {'cat', 'goose', 'lion', 'grizzly'};
weapons = {'fist', 'stick', 'gun', 'grenade'};
low_power_animals = {'cat', 'goose'};
high_power_animals = {'lion', 'grizzly'};
low_power_weapons = {'fist', 'stick'};
high_power_weapons = {'gun', 'grenade'};

% Define stim_subset
stim_subsets = {all_stim, animals, weapons, low_power_animals, high_power_animals, low_power_weapons, high_power_weapons};
subset_names = {'all', 'animals', 'weapons', 'low_power_animals', 'high_power_animals', 'low_power_weapons', 'high_power_weapons'};

% Function to check if a file is readable and not empty
is_readable_file = @(filename) (exist(filename, 'file') && dir(filename).bytes > 4000000);

% Loop through each subset and run the analysis
for i = 1:length(stim_subsets)
    stim_subset = stim_subsets{i};
    subset_name = subset_names{i};
    
    % Filter resultTable by stim_subset
    filteredTable = resultTable(ismember(resultTable.stim, stim_subset), :);

    % Check if filteredTable is empty
    if isempty(filteredTable)
        warning('No data found for subset %s. Skipping...', subset_name);
        continue;
    end

    % Check file readability and exclude unreadable files
    readable_files = cellfun(@(f) is_readable_file(fullfile(data_dir, f)), filteredTable.filename);
    filteredTable = filteredTable(readable_files, :);

    % Check if filteredTable is empty after excluding unreadable files
    if isempty(filteredTable)
        warning('No readable files found for subset %s. Skipping...', subset_name);
        continue;
    end

    % Set the full path to file names for the current subset
    cfg.files.name = strcat(data_dir, filteredTable.filename);

    % Set the chunk and label fields for the current subset
    cfg.files.chunk = filteredTable.chunk;
    cfg.files.label = filteredTable.label;

    % Make the design for cross-validation
    cfg.design = make_design_cv(cfg);
    cfg.design.unbalanced_data = 'ok';

    % Run decoding for the current subset
    results = decoding(cfg);

    % Save results specific to each subset
    subset_results_path = fullfile(results_path, subset_name);
    if ~exist(subset_results_path, 'dir')
        mkdir(subset_results_path); % Create the directory
    end
    save(fullfile(subset_results_path, 'results.mat'), 'results');

    % Plot confusion matrix for the current subset
    figure;
    h = heatmap(results.confusion_matrix.output{1}, 'Colormap', jet);
    unique_labels = unique(cfg.files.label);
    h.XDisplayLabels = string(unique_labels);
    h.YDisplayLabels = string(unique_labels);
    title(['Confusion Matrix for ', subset_name]);
    xlabel('Predicted Labels');
    ylabel('True Labels');
    saveas(gcf, fullfile(subset_results_path, 'confusion_matrix.png'));
end