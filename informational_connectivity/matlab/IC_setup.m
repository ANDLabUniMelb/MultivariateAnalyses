function [stim_path, fig_path, results_path, subids, conditions, rounds, trials_lookup, lookup_table] = IC_setup(name, run_condition)

    date = datestr(now, 'ddmmyy');

    % Set the filepaths using script dir
    script_dir = fileparts(mfilename('fullpath'));
    [project_dir, ~, ~] = fileparts(script_dir);
    stim_path = fullfile(project_dir, 'data', run_condition); % Modified to use run_condition
    
    % Adjust the figure and results saving path to include dataset type
    fig_path = fullfile(project_dir, 'data', 'IC', 'figures', ['figures_', name, '_', run_condition, '_', date]);
    results_path = fullfile(project_dir, 'data', 'IC', 'results', ['results_', name, '_', run_condition, '_', date]);
    lookup_table = readtable(fullfile(project_dir, 'data', 'direction_lookup.csv'));

    % Create the directories if they don't exist
    if ~exist(fig_path, 'dir')
        mkdir(fig_path);
    end

    if ~exist(results_path, 'dir')
        mkdir(results_path);
    end

    % Initialize variables
    rounds_full = {'1', '2', '3', '4'};
    rounds_test = {'1', '2'};
    subids = {'1', '2', '3', '4', '5', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '28', '29', '30', '31'};
    conditions = {'cat', 'goose', 'lion', 'grizzly', 'fist', 'stick', 'gun', 'grenade'};

    % Lookup tables for number of trials per condition (first zstat, second
    % zstat, test files)
    trials_lookup_first = struct(...
        'R1_cat', 4, 'R1_goose', 15, 'R1_lion', 15, 'R1_grizzly', 17, 'R1_fist', 7, 'R1_stick', 15, 'R1_gun', 20, 'R1_grenade', 19, ...
        'R2_cat', 17, 'R2_goose', 8, 'R2_lion', 14, 'R2_grizzly', 13, 'R2_fist', 7, 'R2_stick', 10, 'R2_gun', 18, 'R2_grenade', 14, ...
        'R3_cat', 17, 'R3_goose', 16, 'R3_lion', 10, 'R3_grizzly', 18, 'R3_fist', 15, 'R3_stick', 17, 'R3_gun', 5, 'R3_grenade', 14, ...
        'R4_cat', 18, 'R4_goose', 17, 'R4_lion', 15, 'R4_grizzly', 8, 'R4_fist', 16, 'R4_stick', 14, 'R4_gun', 13, 'R4_grenade', 9);
    
    trials_lookup_second = struct(...
        'R1_cat', 11, 'R1_goose', 17, 'R1_lion', 15, 'R1_grizzly', 18, 'R1_fist', 12, 'R1_stick', 9, 'R1_gun', 11, 'R1_grenade', 17, ...
        'R2_cat', 15, 'R2_goose', 17, 'R2_lion', 15, 'R2_grizzly', 13, 'R2_fist', 12, 'R2_stick', 9, 'R2_gun', 16, 'R2_grenade', 12, ...
        'R3_cat', 15, 'R3_goose', 12, 'R3_lion', 11, 'R3_grizzly', 13, 'R3_fist', 12, 'R3_stick', 9, 'R3_gun', 16, 'R3_grenade', 14, ...
        'R4_cat', 15, 'R4_goose', 10, 'R4_lion', 15, 'R4_grizzly', 12, 'R4_fist', 20, 'R4_stick', 9, 'R4_gun', 13, 'R4_grenade', 13);
    
    trials_lookup_test = struct(...
        'R1_cat', 2, 'R1_goose', 2, 'R1_lion', 2, 'R1_grizzly', 2, 'R1_fist', 2, 'R1_stick', 2, 'R1_gun', 2, 'R1_grenade', 2, ...
        'R2_cat', 2, 'R2_goose', 2, 'R2_lion', 2, 'R2_grizzly', 2, 'R2_fist', 2, 'R2_stick', 2, 'R2_gun', 2, 'R2_grenade', 2, ...
        'R3_cat', 2, 'R3_goose', 2, 'R3_lion', 2, 'R3_grizzly', 2, 'R3_fist', 2, 'R3_stick', 2, 'R3_gun', 2, 'R3_grenade', 2, ...
        'R4_cat', 2, 'R4_goose', 2, 'R4_lion', 2, 'R4_grizzly', 2, 'R4_fist', 2, 'R4_stick', 2, 'R4_gun', 2, 'R4_grenade', 2);
    
    % Depending on the dataset type, use the appropriate trials lookup table
    if strcmp(run_condition, 'first_zstat')
        trials_lookup = trials_lookup_first;
        rounds = rounds_full;
    elseif strcmp(run_condition, 'second_zstat')
        trials_lookup = trials_lookup_second;
        rounds = rounds_full;
    elseif strcmp(run_condition, 'test')
        trials_lookup = trials_lookup_test;
        rounds = rounds_test;
    else
        error('Invalid dataset type specified.');
    end