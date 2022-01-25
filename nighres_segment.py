import nighres
import os
from nilearn import plotting

input_dir = "/home/remi/gin/V5_high-res/pilot_1/derivatives/nighres"
subj = "sub-pilot001"
sess = "ses-001"

subj_dir = os.path.join(input_dir, subj, sess, "anat")

up = "r"
RES = ["075", "069"]

for res in RES:

    inv2 = os.path.join(
        subj_dir, up + "sub-pilot001_ses-001_acq-" + res + "_part-mag_inv-2_MP2RAGE.nii"
    )
    t1w = os.path.join(subj_dir, up + "sub-pilot001_ses-001_acq-" + res + "_UNIT1.nii")
    t1map = os.path.join(
        subj_dir, up + "sub-pilot001_ses-001_acq-" + res + "_T1map.nii"
    )

    skullstripping_results = nighres.brain.mp2rage_skullstripping(
        second_inversion=inv2,
        t1_weighted=t1w,
        t1_map=t1map,
        save_data=True,
        file_name="sub-pilot001_ses-001_acq-" + up + res,
        output_dir=os.path.join(subj_dir, up + res),
    )

    mgdm_results = nighres.brain.mgdm_segmentation(
        contrast_image1=skullstripping_results["t1w_masked"],
        contrast_type1="Mp2rage7T",
        contrast_image2=skullstripping_results["t1map_masked"],
        contrast_type2="T1map7T",
        save_data=True,
        file_name="sub-pilot001_ses-001_acq-" + up + res,
        output_dir=os.path.join(subj_dir, up + res),
    )
