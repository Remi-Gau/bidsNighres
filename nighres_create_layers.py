import nighres
import os
from nilearn import plotting

input_dir = "/home/remi/gin/V5_high-res/pilot_1/derivatives/nighres"
subj = "sub-pilot001"
sess = "ses-001"

subj_dir = os.path.join(input_dir, subj, sess, "anat")

filename = "sub-pilot001_ses-001_acq-"

n_layers = 6

up = ""

RES = ["075", "069"]

for res in RES:

    segmentation = os.path.join(subj_dir, res, filename + res + "_mgdm-seg.nii.gz")
    boundary_dist = os.path.join(subj_dir, res, filename + res + "_mgdm-dist.nii.gz")
    max_labels = os.path.join(subj_dir, res, filename + res + "_mgdm-lbls.nii.gz")
    max_probas = os.path.join(subj_dir, res, filename + res + "_mgdm-mems.nii.gz")

    # extract left cerebrum

    ROIS = ["right_cerebrum", "left_cerebrum"]
    LABELS = ["RightCerebrum", "LeftCerebrum"]

    for i, roi in enumerate(ROIS):

        output_filename = filename + res + "_label-" + LABELS[i] + "_mask"

        cortex = nighres.brain.extract_brain_region(
            segmentation=segmentation,
            levelset_boundary=boundary_dist,
            maximum_membership=max_probas,
            maximum_label=max_labels,
            extracted_region=roi,
            save_data=True,
            file_name=output_filename,
            output_dir=os.path.join(subj_dir, res),
        )

        cruise = nighres.cortex.cruise_cortex_extraction(
            init_image=cortex["inside_mask"],
            wm_image=cortex["inside_proba"],
            gm_image=cortex["region_proba"],
            csf_image=cortex["background_proba"],
            normalize_probabilities=True,
            save_data=True,
            file_name=output_filename,
            output_dir=os.path.join(subj_dir, res, "cruise"),
        )

        depth = nighres.laminar.volumetric_layering(
            inner_levelset=cruise["gwb"],
            outer_levelset=cruise["cgb"],
            n_layers=n_layers,
            save_data=True,
            file_name=output_filename,
            output_dir=os.path.join(subj_dir, res, "nbLayers-" + str(n_layers)),
        )
