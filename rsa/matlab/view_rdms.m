clear
clc

% Set the dataset type here
run_condition = 'first_zstat'; % first_zstat, second_zstat or test
smooth = ''; %'_smooth' or '' if not using smoothed data
date = '190424';

script_dir = fileparts(mfilename('fullpath'));
% [project_dir, ~, ~] = fileparts(script_dir);
% results_dir = fullfile(project_dir, 'results', ['results_', date]);

% Adjust the figure and results saving path to include dataset type
results_path = fullfile(script_dir, 'RDMs_insula.mat');
fprintf(results_path);
load(results_path);
