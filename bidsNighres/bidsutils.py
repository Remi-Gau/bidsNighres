import json
from os.path import abspath
from os.path import dirname
from os.path import join
from pathlib import Path

from bids import BIDSLayout
from rich import print

from .utils import create_dir_if_absent
from .utils import move_file


def get_dataset_layout(dataset_path: str, config={}):

    create_dir_if_absent(dataset_path)

    if config == {}:
        pybids_config = get_pybids_config()

    layout = BIDSLayout(
        dataset_path, validate=False, derivatives=False, config=pybids_config
    )
    return layout


def write_dataset_description(layout):

    output_file = join(layout.root, "dataset_description.json")

    with open(output_file, "w") as ff:
        json.dump(layout.dataset_description, ff, indent=4)


def set_dataset_description(layout, is_derivative=True):

    data = {
        "Name": "dataset name",
        "BIDSVersion": "1.6.0",
        "DatasetType": "raw",
        "License": "",
        "Authors": ["", ""],
        "Acknowledgements": "Special thanks to ",
        "HowToAcknowledge": "Please cite this paper: ",
        "Funding": ["", ""],
        "EthicsApprovals": [""],
        "ReferencesAndLinks": ["", ""],
        "DatasetDOI": "doi:",
        "HEDVersion": "",
    }

    if is_derivative:
        data["GeneratedBy"] = [
            {
                "Name": "",
                "Version": "",
                "Container": {"Type": "", "Tag": ""},
                "Description": "",
                "CodeURL": "",
            },
        ]

        data["SourceDatasets"] = [
            {
                "DOI": "doi:",
                "URL": "",
                "Version": "",
            }
        ]

    layout.dataset_description = data

    return layout


def init_derivatives_layout(output_location):
    layout_out = get_dataset_layout(output_location)
    layout_out = set_dataset_description(layout_out)
    layout_out.dataset_description["DatasetType"] = "derivative"
    layout_out.dataset_description["GeneratedBy"][0]["Name"] = "bidsNighres"
    write_dataset_description(layout_out)
    return layout_out


def get_bidsname_config(config_file="") -> dict:
    """
    See the Path construction demo in the pybids tuto
    https://github.com/bids-standard/pybids/blob/master/examples/pybids_tutorial.ipynb
    """
    default = "config_bidsname.json"
    return get_config(config_file, default)


def get_pybids_config(config_file="") -> dict:
    """
    Pybids configs are stored in the layout module
    https://github.com/bids-standard/pybids/tree/master/bids/layout/config
    """
    default = "config_pybids.json"
    return get_config(config_file, default)


def get_bids_filter_config(config_file="") -> dict:
    default = "default_filter_file.json"
    return get_config(config_file, default)


def get_config(config_file="", default="") -> dict:

    if config_file == "" or not Path(config_file).exists():
        my_path = dirname(abspath(__file__))
        config_file = join(my_path, default)

    if config_file == "" or not Path(config_file).exists():
        return
    with open(config_file, "r") as ff:
        return json.load(ff)


def bidsify_skullstrip_output(
    skullstrip_output, layout_in, layout_out, UNIT1, inv2, T1map, dry_run=True
):

    entities = layout_in.parse_file_entities(UNIT1)
    entities["extension"] = ".nii.gz"
    brain_mask = create_bidsname(layout_out, entities, filetype="mask")
    move_file(skullstrip_output["brain_mask"], brain_mask, dry_run=dry_run)
    skullstrip_output["brain_mask"] = brain_mask

    outputs = ["inv2_masked", "t1w_masked", "t1map_masked"]
    inputs = [inv2, UNIT1, T1map]

    for i, o in zip(inputs, outputs):
        entities = layout_in.parse_file_entities(i)
        entities["extension"] = ".nii.gz"
        new_output = create_bidsname(layout_out, entities, filetype="skullstripped")
        move_file(skullstrip_output[o], new_output, dry_run=dry_run)
        skullstrip_output[o] = new_output

    return skullstrip_output


# Returns:

# Dictionary collecting outputs under the following keys (suffix of output files in brackets)

#  outputs = ["segmentation", "labels", "memberships", "distance"]
#
#     "segmentation" (niimg): Hard brain segmentation with topological constraints (if chosen)
#                          (_mgdm_seg)
#     "labels" (niimg):      Maximum tissue probability labels
#                          (_mgdm_lbls)
#     "memberships" (niimg): Maximum tissue probability values,
#                          4D image where the first dimension shows each voxel’s highest
#                          probability to belong to a specific tissue,
#                          the second dimension shows the second highest probability to
#                          belong to another tissue etc.
#                         (_mgdm_mems)
#     "distance" (niimg):   Minimum distance to a segmentation boundary
#                         (_mgdm_dist)


def create_bidsname(layout, filename, filetype: str) -> str:
    # filename is path or entities dict

    if isinstance(filename, str):
        entities = layout.parse_file_entities(filename)
    else:
        entities = filename

    bids_name_config = get_bidsname_config()
    output_file = layout.build_path(
        entities, bids_name_config[filetype], validate=False
    )

    output_file = abspath(join(layout.root, output_file))

    return output_file


def check_layout(layout):

    bf = layout.get(
        return_type="filename",
        suffix="^MP2RAGE$",
        extension="nii.*",
        regex_search=True,
    )

    if bf == []:
        raise Exception("Input dataset does not have any data to process")
