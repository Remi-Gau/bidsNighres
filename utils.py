import os
from os.path import abspath
from os.path import dirname
from pathlib import Path

from bids import BIDSLayout
from rich import print


def move_file(input: str, output: str):

    print(f"{abspath(input)} --> {abspath(output)}")
    create_dir_for_file(output)
    os.rename(input, output)


def get_dataset_layout(dataset_path: str):

    create_dir_if_absent(dataset_path)

    layout = BIDSLayout(dataset_path, validate=False, derivatives=False)
    return layout


def return_regex(string):
    return f"^{string}$"


def create_dir_if_absent(output_path: str):
    if not Path(output_path).exists():
        print(f"Creating dir: {output_path}")
        os.makedirs(output_path)


def create_dir_for_file(file: str):
    output_path = dirname(abspath(file))
    create_dir_if_absent(output_path)
