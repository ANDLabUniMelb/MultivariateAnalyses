%% Description
% This function specifies the DCMs to estimate.

function dcm_spec_extinction(subject_id, version, task_num, condition, spec)
%% SET UP
spm('Defaults', 'fMRI');
spm_jobman('initcfg');
spm_get_defaults('cmdline', true);

task_num_str = num2str(task_num);
fear_task = ['fear_', task_num_str];
folder = [fear_task, '_', condition];

conditions = {'Task', ...
    ['CS+', condition], ['CS-', condition], ...
    'Fixation', 'Question', 'Scream', ...
    };
include = [1 1 1 0 0 0]';   % only include first three conditions

% Set DCM analysis parameters
TR = 3; % Repetition Time
TE = 0.04;  % Echo time in seconds
nregions    = 4; 
nconditions = sum(include); % Number of original conditions
hipp=1; postvmpfc=2; amygdala=3; striatum=4; % index rois

% define filepaths
if subject_id == 1000
    subject_id_str = '1000';
else
    subject_id_str = sprintf('%03d', subject_id);
end

output_dir     = fullfile('/data/gpfs/projects/punim2239/panda/data/output', version, folder);
spm_dir = fullfile(output_dir, subject_id_str);

%% DEFINE MATRICES
a = zeros(nregions,nregions);
a(striatum,  amygdala)  = 1;
a(amygdala,  striatum)  = 1;
% 
a(striatum,  hipp)      = 1;
a(striatum,  postvmpfc) = 1;

a(postvmpfc, striatum) = 1;

% Limbic and cortical loops
a(amygdala,  postvmpfc) = 1;
a(postvmpfc, amygdala)  = 1;
% 
a(amygdala,  hipp)      = 1;
a(hipp,      amygdala)  = 1;

a(postvmpfc, hipp)      = 1;
a(hipp, postvmpfc)      = 1;

c = zeros(nregions,nconditions); % C-matrix (driving input = task)
c(:,1) = 1; % task condition = 1 driving input for all regions

d = zeros(nregions, nregions, 0);  % D-matrix (disabled)

% Pre-allocate B-matrix
b = zeros(nregions, nregions, nconditions);

% Loop over conditions
for cond = 2:nconditions
    % Threat connections
    b(postvmpfc, hipp, cond)     = 1;   % +: Hippocampus → Posterior VMPFC
    b(striatum, amygdala, cond)     = 1;   % +: Amygdala → Striatum
    b(amygdala, postvmpfc, cond)    = 1;   % +: Posterior VMPFC → Amygdala
end

%% LOAD VOIs
SPM = load(fullfile(spm_dir, 'SPM.mat')); 
SPM = SPM.SPM;

voi_files = { ...
    fullfile(spm_dir, ['VOI_hipp_', subject_id_str, '_1.mat']), ...
    fullfile(spm_dir, ['VOI_postvmpfc_', subject_id_str, '_1.mat']), ...
    fullfile(spm_dir, ['VOI_amygdala_', subject_id_str, '_1.mat']), ...
    fullfile(spm_dir, ['VOI_striatum_', subject_id_str, '_1.mat'])};

for r = 1:length(voi_files)
    XY = load(voi_files{r});    % VOI.xY is the struct, VOI.Y is the single timeseries
    xY_temp = XY.xY;              % copy the existing fields (name, Sess, etc.)
    xY_temp.xY = XY.Y;            % overwrite the .xY field with the single-column time series
    xY(r) = xY_temp;
end

%% Specify the DCM structure (common fields)
s = struct();
s.name       = subject_id_str;
s.u          = include;     % Include conditions
s.delays     = repmat(TR/2, 1, nregions);  % Slice timing for each region
s.TE         = TE;
s.nonlinear  = false; % bilinear
s.two_state  = false; % one-state
s.stochastic = false; % non-stochastic
s.centre     = true;
s.induced    = 0;
s.a          = a;
s.b          = b;
s.c          = c;
s.d          = d;
s.name       = subject_id_str;  % Adjust the model name
DCM = spm_dcm_specify(SPM, xY, s);

save(fullfile(spm_dir, ['DCM_', spec, '_', subject_id_str, '.mat']), 'DCM');
end