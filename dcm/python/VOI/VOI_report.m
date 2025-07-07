%% Fill me in
clear 

subjects = [100;101;102;103;104;106;107;108;109;111;112;113;114;116;117;118;119;120;121;122;123;125;126;127;128;130;131;132;133;134;135;137;138;139;140;142;143;145;146;147;148;149;150;151;152;153;154;156];

rootdir= '/data/scratch/projects/punim1471/NeuroWIRED/DCM/1st_DCM/';

%name you regions in order, Hb not needed
regions={'sgACC','dACC','Caudate','PCC'};

%name your target coordinates xyz in order
targets={[-3 22 -18],[-6 21 38],[-11 8 8],[5 -45 34]};

%% Pull xyz and eigen values

for ri =1:length(regions) %ri is region index
    VOI(ri).name=regions(ri);
    VOI(ri).targets=targets(ri);
    VOI(ri).out=zeros(length(subjects),2);
    VOI(ri).out(:,1)=subjects(:);
end

for ri=1:length(regions)
    xyz=zeros(length(subjects),4);

    for i= 1:length(subjects) %i is subject index
    sub=num2str(subjects(i));
    
    VOI_path=[rootdir, sub, '/VOI_' VOI(ri).name{1,1} '_' sub '_1.mat'];
    
        if exist(VOI_path,'file')==2
        load (VOI_path)
        xyz(i,1)=subjects(i);
        xyz(i,2:4)=xY.xyz';
        eigen(i,1)=100*xY.s(1)/sum(xY.s);
        else
        xyz(i,1)=subjects(i);
        xyz(i,2:4)=[99 99 99]; %% Label missing VOIs with 99 99 99
        eigen(i,1)=99;

        end
    VOI(ri).xyz=xyz;
    VOI(ri).eigen=mean(eigen);
    end
end
%% Compare targets 
for ri=1:length(regions)
    for i=1:length(subjects)
        
        if VOI(ri).xyz(i,2)>(VOI(ri).targets{1,1}(1)+8.9) ||...
                VOI(ri).xyz(i,2)<(VOI(ri).targets{1,1}(1)-8.9)
            VOI(ri).out(i,2)=99; %% 99 is out
        elseif VOI(ri).xyz(i,3)>(VOI(ri).targets{1,1}(2)+8.9) ||...
                VOI(ri).xyz(i,3)<(VOI(ri).targets{1,1}(2)-8.9)
            VOI(ri).out(i,2)=99; %% 99 is out
        elseif VOI(ri).xyz(i,4)>(VOI(ri).targets{1,1}(3)+8.9) ||...
                VOI(ri).xyz(i,4)<(VOI(ri).targets{1,1}(3)-8.9)
            VOI(ri).out(i,2)=99; %% 99 is out
            
        else VOI(ri).out(i,2)=1; % 1 is in
        
        end

    end
end

%% Provide total count and participant vector
for ri=1:length(regions) 
    out_row=find(VOI(ri).out(:,2)==99);
    VOI(ri).subs_out=VOI(ri).out(out_row);
    writematrix(VOI(ri).subs_out',['Out_subs_' num2str(ri) '.txt'])
end
    VOI(1).all_out_subs=unique(cat(1,VOI(:).subs_out));
    
save('VOI_report.mat','VOI');
