#!/usr/bin/env python3
import os
import subprocess
from glob import glob
from html import entities

import click
import nibabel
import numpy
from bids import BIDSLayout
from matplotlib.pyplot import table
from rich import print

__version__ = open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "version")
).read()


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
    type=click.Choice(["genT1map", "skullstripping", "segment"], case_sensitive=False),
)
def main(input_datasets, output_location, analysis_level, participant_label, action):

    input_datasets = os.path.abspath(input_datasets)
    output_location = os.path.abspath(output_location)

    print(input_datasets)
    print(output_location)
    print(analysis_level)
    print(participant_label)

    layout = BIDSLayout(input_datasets)

    print(layout.get_subjects())
    print(layout.get_sessions())
    unit1_files = layout.get(
        subject=participant_label,
        suffix="UNIT1",
        extension="nii",
        regex_search=True,
    )

    for t1 in unit1_files:

        entities = t1.get_entities()
        print(entities)
        print(t1.filename)

        inv2 = layout.get(
            return_type="filename",
            subject=participant_label,
            inv=2,
            acquisition=entities["acquisition"],
            suffix="MP2RAGE",
            extension="nii",
            regex_search=True,
        )
        print(inv2)

        t1map = layout.get(
            return_type="filename",
            subject=participant_label,
            acquisition=entities["acquisition"],
            suffix="T1map",
            extension="nii",
            regex_search=True,
        )
        print(t1map)


# parser.add_argument('-v', '--version', action='version',
#                     version='bidsNighRes {}'.format(__version__))

# subjects_to_analyze = []
# # only for a subset of subjects
# if args.participant_label:
#     subjects_to_analyze = args.participant_label
# # for all subjects
# else:
#     subject_dirs = glob(os.path.join(args.bids_dir, "sub-*"))
#     subjects_to_analyze = [subject_dir.split("-")[-1] for subject_dir in subject_dirs]

# # running participant level
# if args.analysis_level == "participant":

#     # find all T1s and skullstrip them
#     for subject_label in subjects_to_analyze:
#         for T1_file in glob(os.path.join(args.bids_dir, "sub-%s"%subject_label,
#                                          "anat", "*_T1w.nii*")) + glob(os.path.join(args.bids_dir,"sub-%s"%subject_label,"ses-*","anat", "*_T1w.nii*")):
#             out_file = os.path.split(T1_file)[-1].replace("_T1w.", "_brain.")
#             cmd = "bet %s %s"%(T1_file, os.path.join(args.output_dir, out_file))
#             print(cmd)
#             run(cmd)

# # running group level
# elif args.analysis_level == "group":
#     brain_sizes = []
#     for subject_label in subjects_to_analyze:
#         for brain_file in glob(os.path.join(args.output_dir, "sub-%s*.nii*"%subject_label)):
#             data = nibabel.load(brain_file).get_data()
#             # calcualte average mask size in voxels
#             brain_sizes.append((data != 0).sum())

#     with open(os.path.join(args.output_dir, "avg_brain_size.txt"), 'w') as fp:
#         fp.write("Average brain size is %g voxels"%numpy.array(brain_sizes).mean())


def return_regex(string):
    return f"^{string}$"


if __name__ == "__main__":
    main()
