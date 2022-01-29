import os
from os.path import abspath
from os.path import dirname
from pathlib import Path

from rich import print


def move_file(input: str, output: str, dry_run=False):

    print(f"{abspath(input)} --> {abspath(output)}")
    if not dry_run:
        create_dir_for_file(output)
        os.rename(input, output)


def return_regex(string):
    return f"^{string}$"


def create_dir_if_absent(output_path: str):
    if not Path(output_path).exists():
        print(f"Creating dir: {output_path}")
        os.makedirs(output_path)


def create_dir_for_file(file: str):
    output_path = dirname(abspath(file))
    create_dir_if_absent(output_path)


def return_path_rel_dataset(file_path: str, dataset_path: str) -> str:
    """
    Create file path relative to the root of a dataset
    """
    file_path = abspath(file_path)
    dataset_path = abspath(dataset_path)
    rel_path = file_path.replace(dataset_path, "")
    rel_path = rel_path[1:]
    return rel_path
