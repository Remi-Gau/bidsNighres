import os
from pathlib import Path

from bidsNighres.bidsutils import bidsify_skullstrip_output
from bidsNighres.bidsutils import create_bidsname
from bidsNighres.bidsutils import get_dataset_layout
from bidsNighres.bidsutils import init_derivatives_layout
from bidsNighres.utils import return_path_rel_dataset


def test_write_dataset_description():

    output_location = Path().resolve()
    output_location = Path.joinpath(output_location, "derivatives")

    layout_out = init_derivatives_layout(output_location)


def test_create_bidsname():

    output_location = Path().resolve()
    output_location = Path.joinpath(output_location, "derivatives")

    layout = get_dataset_layout(output_location)
    filename = (
        "inputs/raw/sub-pilot001/ses-001/anat/sub-pilot001_ses-001_acq-hires_UNIT1.nii"
    )

    output_file = create_bidsname(layout, filename=filename, filetype="mask")

    rel_path = return_path_rel_dataset(file_path=output_file, dataset_path=layout.root)
    assert (
        rel_path
        == "sub-pilot001/ses-001/anat/sub-pilot001_ses-001_acq-hires_desc-brain_mask.nii"
    )


def test_bidsify_skullstrip_output():

    input_location = Path.joinpath(Path().resolve(), "raw")
    output_location = Path.joinpath(input_location, "derivatives")

    layout_in = get_dataset_layout(input_location)
    layout_out = get_dataset_layout(output_location)

    UNIT1 = "sub-01/sub-01_ses-01_UNIT1.nii"
    inv2 = "sub-01/sub-01_ses-01_inv-2_part-mag_MP2RAGE.nii"
    T1map = "sub-01/sub-01_ses-01_T1map.nii"

    skullstrip_output = {
        "t1w_masked": "sub-01_ses-01_UNIT1.nii",
        "inv2_masked": "sub-01_ses-01_inv-2_part-mag_MP2RAGE.nii",
        "t1map_masked": "sub-01_ses-01_UNIT1.nii",
        "brain_mask": "sub-01_ses-01_UNIT1.nii",
    }

    skullstrip_new_output = bidsify_skullstrip_output(
        skullstrip_output,
        layout_in=layout_in,
        layout_out=layout_out,
        UNIT1=UNIT1,
        inv2=inv2,
        T1map=T1map,
    )

    assert (
        os.path.basename(skullstrip_new_output["brain_mask"])
        == "sub-01_ses-01_desc-brain_mask.nii.gz"
    )
    assert (
        os.path.basename(skullstrip_new_output["t1w_masked"])
        == "sub-01_ses-01_desc-skullstripped_UNIT1.nii.gz"
    )
    assert (
        os.path.basename(skullstrip_new_output["t1map_masked"])
        == "sub-01_ses-01_desc-skullstripped_T1map.nii.gz"
    )
    assert (
        os.path.basename(skullstrip_new_output["inv2_masked"])
        == "sub-01_ses-01_inv-2_part-mag_desc-skullstripped_MP2RAGE.nii.gz"
    )


def test_parse_unit1():

    UNIT1 = ["/foo/sub-01/sub-01_ses-01_UNIT1.nii"]
    input_location = Path.joinpath(Path().resolve(), "raw")
    layout_in = get_dataset_layout(input_location)
    entities = layout_in.parse_file_entities(UNIT1[0])
    assert entities == {
        "subject": "01",
        "extension": ".nii",
        "session": "01",
        "suffix": "UNIT1",
    }


def test_parse_inv2():

    inv2 = ["/foo/sub-01/sub-01_ses-01_inv-2_part-mag_MP2RAGE.nii"]
    input_location = Path.joinpath(Path().resolve(), "raw")
    layout_in = get_dataset_layout(input_location)
    entities = layout_in.parse_file_entities(inv2[0])
    assert entities == {
        "subject": "01",
        "extension": ".nii",
        "session": "01",
        "suffix": "MP2RAGE",
        "inv": "2",
        "part": "mag",
    }


def test_parse_T1map():

    T1map = ["/foo/sub-01/sub-01_ses-01_T1map.nii"]
    input_location = Path.joinpath(Path().resolve(), "raw")
    layout_in = get_dataset_layout(input_location)
    entities = layout_in.parse_file_entities(T1map[0])
    assert entities == {
        "subject": "01",
        "extension": ".nii",
        "session": "01",
        "suffix": "T1map",
    }


def test_parse_desc():

    T1map = [
        "bidsNighres/sub-01/ses-01/anat/sub-01_ses-01_inv-2_part-mag_desc-skullstripped_MP2RAGE.nii.gz"
    ]

    input_location = Path.joinpath(Path().resolve(), "derivatives")
    layout_in = get_dataset_layout(input_location)
    entities = layout_in.parse_file_entities(T1map[0])
    assert entities == {
        "subject": "01",
        "datatype": "anat",
        "inv": "2",
        "part": "mag",
        "extension": ".nii.gz",
        "session": "01",
        "description": "skullstripped",
        "suffix": "MP2RAGE",
    }
