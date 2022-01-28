#!/usr/bin/env python3
import os
import subprocess
from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import realpath

import click
from rich import print

from segment import segment
from utils import get_dataset_layout

__version__ = open(join(dirname(realpath(__file__)), "version")).read()


def run(command, env={}):
    merged_env = os.environ
    merged_env.update(env)
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        env=merged_env,
    )
    while True:
        line = process.stdout.readline()
        line = str(line, "utf-8")[:-1]
        print(line)
        if line == "" and process.poll() != None:
            break
    if process.returncode != 0:
        raise Exception("Non zero return code: %d" % process.returncode)


@click.command()
@click.option(
    "--input-datasets",
    help="""
            The directory with the input dataset formatted according to the BIDS standard.
            """,
    type=click.Path(exists=True, dir_okay=True),
)
@click.option(
    "--output-location",
    help="""
            The directory where the output files should be stored.
            If you are running group level analysis this folder should be prepopulated
            with the results of the participant level analysis.
            """,
    type=click.Path(exists=False, dir_okay=True),
)
@click.option(
    "--analysis-level",
    help="""
            Level of the analysis that will be performed.
            Multiple participant level analyses can be run independently
            (in parallel) using the same output-location.
            """,
    type=click.Choice(["participant", "group"], case_sensitive=True),
)
@click.option(
    "--participant-label",
    help="""
            The label(s) of the participant(s) that should be analyzed. The label
            corresponds to sub-<participant_label> from the BIDS spec
            (so it does not include "sub-"). If this parameter is not
            provided all subjects should be analyzed. Multiple
            participants can be specified with a space separated list.
            """,  # nargs ?
)
@click.option(
    "--action",
    help="""
            What to do
            """,
    type=click.Choice(["genT1map", "skullstrip", "segment"], case_sensitive=False),
)
def main(input_datasets, output_location, analysis_level, participant_label, action):

    input_datasets = abspath(input_datasets)
    output_location = abspath(output_location)

    print(f"Input dataset: {input_datasets}")

    print(f"Output location: {output_location}")

    if action == "skullstrip":

        layout_in = get_dataset_layout(input_datasets)

        layout_out = get_dataset_layout(output_location)

        # print(layout.get_subjects())

        # print(layout.get_sessions())

        # TODO add loop for subjects

        segment(layout_in, layout_out, participant_label)


# parser.add_argument('-v', '--version', action='version',
#                     version='bidsNighRes {}'.format(__version__))

if __name__ == "__main__":
    main()
