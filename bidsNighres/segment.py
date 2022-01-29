from os.path import join

import nighres
from rich import print

from bidsNighres.bidsutils import bidsify_skullstrip_output


def skullstrip(layout_in, layout_out, this_participant):

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

        # use filter file to select only lores
        entities["acquisition"] = "lores"

        output_dir = join(layout_out.root, sub_entity, ses_entity, "anat")

        UNIT1 = layout_in.get(
            return_type="filename",
            subject=this_participant,
            acquisition=entities["acquisition"],
            suffix="UNIT1",
            extension="nii",
            regex_search=True,
        )
        print(UNIT1)

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

        T1map = layout_in.get(
            return_type="filename",
            subject=this_participant,
            suffix="T1map",
            extension="nii",
            regex_search=True,
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
