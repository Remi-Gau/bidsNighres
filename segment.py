from os.path import join

import nighres
from rich import print

from utils import move_file


def segment(layout_in, layout_out, this_participant):

    print(f"Processing: {this_participant}")

    # print(layout_in.get_subjects())

    # print(layout_in.get_sessions())

    # TODO add loop for subjects

    unit1_files = layout_in.get(
        subject=this_participant,
        suffix="UNIT1",
        extension="nii",
        regex_search=True,
    )

    sub_entity = "sub-" + this_participant
    ses_entity = "ses-" + "001"

    for bf in unit1_files:

        entities = bf.get_entities()

        entities["acquisition"] = "lores"

        output_dir = join(layout_out.root, sub_entity, ses_entity, "anat")

        t1w = layout_in.get(
            return_type="filename",
            subject=this_participant,
            acquisition=entities["acquisition"],
            suffix="UNIT1",
            extension="nii",
            regex_search=True,
        )
        print(t1w)

        inv2 = layout_in.get(
            return_type="filename",
            subject=this_participant,
            inv=2,
            acquisition=entities["acquisition"],
            suffix="MP2RAGE",
            extension="nii",
            regex_search=True,
        )
        print(inv2)

        t1map = layout_in.get(
            return_type="filename",
            subject=this_participant,
            suffix="T1map",
            extension="nii",
            regex_search=True,
        )
        print(t1map)

        skullstrip_output = nighres.brain.mp2rage_skullstripping(
            second_inversion=inv2[0],
            t1_weighted=t1w[0],
            t1_map=t1map[0],
            save_data=True,
            file_name=sub_entity + "_" + ses_entity + "_desc-",
            output_dir=output_dir,
        )

        # use pybids CONFIG to help generate pybids filenames
        # rename output to be BIDS derivatives compliant
        brain_mask = (
            skullstrip_output["brain_mask"]
            .replace("-_", "-")
            .replace("strip-", "brain_")
        )
        move_file(skullstrip_output["brain_mask"], brain_mask)

        for output in ["t1w_masked", "inv2_masked", "t1map_masked"]:
            new_output = (
                skullstrip_output[output].replace("-_", "-").replace("strip-", "strip_")
            )
            move_file(skullstrip_output[output], new_output)

        # TODO generate JSON for derivatives
        # import json
        # data = {'field1': 'value1', 'field2': 3, 'field3': 'field3'}
        # with open('my_output_file.json', 'w') as ff:
        #     json.dump(data, ff)
