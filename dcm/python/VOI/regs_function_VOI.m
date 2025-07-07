%% Three inputs are needed. 
%First an array with your subject IDs, 
%next your chosen threshold (see below) and last, 
%your region to run the VOI extraction on. Use 99 as an input to run all
%regions

function regs_function_VOI(array_number, thresh_input, region_select)

subject = num2str(array_number);
group = 'Controls';

% Determine Hb mask binarising threshold for each subject based on vol.csv
load("bin_list.mat");
id = ismember(bin_list(:,1),array_number);
thr = num2str(bin_list(id,2));

%name you regions in order
regions={'Hb','sgACC','dACC','Caudate','PCC'};

%name your target coordinates xyz in order (Hb represented with place
%holder 3 -21 3)
targets={[3 -21 3],[-3 22 -18],[-6 21 38],[-11 8 8],[5 -45 34]};

%path to your SPM files
rootdir= '/data/scratch/projects/punim1471/NeuroWIRED/DCM/1st_DCM/';

%set your thresholds
thresh(1)= 0.001;
thresh(2)= 0.01;
thresh(3)= 0.05; %conventional
thresh(4)= 0.1;
thresh(5)= 0.15;
thresh(6)= 0.2;
thresh(7)= 0.25;
thresh(8)= 0.3;
thresh(9)= 0.35;
thresh(10)= 0.4;
thresh(11)= 0.45;
thresh(12)= 0.5;

%Use 99 as the region_select input to run through all regions
if region_select==99 
    x=length(regions);
    y=1;
else
    x=region_select;
    y=region_select;
end

%% Run batch

%Initialize SPM
spm_jobman('initcfg');
    for ri = y:x   %region index

    if ri == 1
matlabbatch{1}.spm.util.voi.spmmat(1) = {[rootdir, subject, '/SPM.mat']};
matlabbatch{1}.spm.util.voi.adjust = 1; % Adjust data for [effects of interest], enter index for F-contrast created above; 0 for no adjustment; NaN adjust for everything
matlabbatch{1}.spm.util.voi.session = 1;
matlabbatch{1}.spm.util.voi.name = [regions{ri}, '_' ,subject];
matlabbatch{1}.spm.util.voi.roi{1}.spm.spmmat = {''};
matlabbatch{1}.spm.util.voi.roi{1}.spm.contrast = 2; % 1=EoF, 2=Task, 3=CHAL, 4=REP, 5=CHAL>REP, 6=REP>CHAL
matlabbatch{1}.spm.util.voi.roi{1}.spm.conjunction = 1;
matlabbatch{1}.spm.util.voi.roi{1}.spm.threshdesc = 'none';
matlabbatch{1}.spm.util.voi.roi{1}.spm.thresh = thresh(thresh_input); %convention is .05 (end of Ziedmann 2019 p1)
matlabbatch{1}.spm.util.voi.roi{1}.spm.extent = 0; %common to use 0, deciding on the number of voxels to classify as VOI
matlabbatch{1}.spm.util.voi.roi{1}.spm.mask = struct('contrast', {}, 'thresh', {}, 'mtype', {});
matlabbatch{1}.spm.util.voi.roi{2}.mask.image = {['/data/scratch/projects/punim1471/NeuroWIRED/Hb_segmentation/Hb_labels_t1/CNBT/PPI_ROI/bin' thr '_wrs_brain' subject '_t1_labels_rmCSF.nii,1']};
matlabbatch{1}.spm.util.voi.roi{2}.mask.threshold = 0.5;
matlabbatch{1}.spm.util.voi.expression = 'i1 & i2'; %extract masked region (pt2) from thresholded VOI (pt1)
    
    else
matlabbatch{1}.spm.util.voi.spmmat(1) = {[rootdir, subject, '/SPM.mat']};
matlabbatch{1}.spm.util.voi.adjust = 1; % Adjust data for [effects of interest], enter index for F-contrast created above; 0 for no adjustment; NaN adjust for everything
matlabbatch{1}.spm.util.voi.session = 1;
matlabbatch{1}.spm.util.voi.name = [regions{ri}, '_' ,subject];
matlabbatch{1}.spm.util.voi.roi{1}.spm.spmmat = {''};
matlabbatch{1}.spm.util.voi.roi{1}.spm.contrast = 2; % 1=EoF, 2=Task, 3=CHAL, 4=REP, 5=CHAL>REP, 6=REP>CHAL
matlabbatch{1}.spm.util.voi.roi{1}.spm.conjunction = 1;
matlabbatch{1}.spm.util.voi.roi{1}.spm.threshdesc = 'none';
matlabbatch{1}.spm.util.voi.roi{1}.spm.thresh = thresh(thresh_input); %convention is .05 (end of Ziedmann 2019 p1)
matlabbatch{1}.spm.util.voi.roi{1}.spm.extent = 0; %common to use 0, deciding on the number of voxels to classify as VOI
matlabbatch{1}.spm.util.voi.roi{1}.spm.mask = struct('contrast', {}, 'thresh', {}, 'mtype', {});
matlabbatch{1}.spm.util.voi.roi{2}.sphere.centre = targets{ri}; %ri = region index, calling specific coordinates
matlabbatch{1}.spm.util.voi.roi{2}.sphere.radius = 4; %mm radius of VOI (Zeidmann 2019)
matlabbatch{1}.spm.util.voi.roi{2}.sphere.move.local.spm = 1; %nearest local max. spm index
matlabbatch{1}.spm.util.voi.roi{2}.sphere.move.local.mask = '';
matlabbatch{1}.spm.util.voi.expression = 'i1 & i2'; %extract sphere (pt2) from thresholded VOI (pt1)
    
    end
    
end
    
spm_jobman('run', matlabbatch);
