

% inv2 = os.path.join(
%     subj_dir, "sub-pilot001_ses-001_acq-" + res + "_part-mag_inv-2_MP2RAGE.nii.gz"
% )
% t1w = os.path.join(subj_dir, "sub-pilot001_ses-001_acq-" + res + "_UNIT1.nii")
% t1map = os.path.join(subj_dir, "sub-pilot001_ses-001_acq-" + res + "_T1map.nii")
% 
% names{1} = 'sub-pilot001_ses-001_acq-%s_part-mag_inv-2_MP2RAGE';
% names{2} = 'sub-pilot001_ses-001_acq-%s_UNIT1';

res = '069';

der_folder = fullfile(pwd, '..', '..', 'derivatives', 'nighres', 'sub-pilot001', 'ses-001', 'anat');

img{1,1} = spm_select('FPlist', der_folder, ['^.*' res '_UNIT1.*.nii$']);
img{2,1} = spm_select('FPlist', der_folder, ['^.*' res '_T1map.*.nii$']);
img{3,1} = spm_select('FPlist', der_folder, ['^.*' res '_part-mag_inv-2_MP2RAGE.nii$']);

for i = 1: numel(img)
resize_img(img{i}, [0.5 0.5 0.5], nan(2,3), false())
end