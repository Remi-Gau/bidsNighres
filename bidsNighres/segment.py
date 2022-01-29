from os.path import join

import nighres
from rich import print

from bidsNighres.bidsutils import bidsify_skullstrip_output


def skullstrip(layout_in, layout_out, this_participant, bids_filter: dict):

    print(f"Processing: {this_participant}")

    # print(layout_in.get_subjects())

    # print(layout_in.get_sessions())

    unit1_files = layout_in.get(
        subject=this_participant,
        extension="nii",
        regex_search=True,
        **bids_filter["UNIT1"],
    )

    sub_entity = "sub-" + this_participant
    ses_entity = "ses-" + "001"

    for bf in unit1_files:

        entities = bf.get_entities()

        # use filter file to select only lores
        entities["acquisition"] = "lores"

        output_dir = join(layout_out.root, sub_entity, ses_entity, "anat")

        UNIT1 = layout_in.get(
            return_type="filename",
            subject=this_participant,
            extension="nii",
            regex_search=True,
            **bids_filter["UNIT1"],
        )
        print(UNIT1)

        inv2 = layout_in.get(
            return_type="filename",
            subject=this_participant,
            extension="nii",
            regex_search=True,
            **bids_filter["inv2"],
        )
        print(inv2)

        T1map = layout_in.get(
            return_type="filename",
            subject=this_participant,
            extension="nii",
            regex_search=True,
            **bids_filter["T1map"],
        )
        print(T1map)

        skullstrip_output = nighres.brain.mp2rage_skullstripping(
            second_inversion=inv2[0],
            t1_weighted=UNIT1[0],
            t1_map=T1map[0],
            save_data=True,
            file_name=sub_entity + "_" + ses_entity + "_desc-",
            output_dir=output_dir,
        )

        bidsify_skullstrip_output(
            skullstrip_output,
            layout_in=layout_in,
            layout_out=layout_out,
            UNIT1=UNIT1[0],
            inv2=inv2[0],
            T1map=T1map[0],
            dry_run=False,
        )

        # TODO generate JSON for derivatives
        # import json
        # data = {'field1': 'value1', 'field2': 3, 'field3': 'field3'}
        # with open('my_output_file.json', 'w') as ff:
        #     json.dump(data, ff)

    # mgdm_results = nighres.brain.mgdm_segmentation(
    #     contrast_image1=skullstripping_results["t1w_masked"],
    #     contrast_type1="Mp2rage7T",
    #     contrast_image2=skullstripping_results["t1map_masked"],
    #     contrast_type2="T1map7T",
    #     save_data=True,
    #     file_name="sub-pilot001_ses-001_acq-" + up + res,
    #     output_dir=os.path.join(subj_dir, up + res),
    # )
