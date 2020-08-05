# CRC nighres

For processing of high-res images from the [CRC](https://www.campus.uliege.be/cms/c_1841124/fr/b30-centre-de-recherches-du-cyclotron-crc) using [nighres](https://nighres.readthedocs.io/en/latest/).

## Data structure

Assumes a BIDS.

More specifically the one described by the BEP-001 of BIDS

https://bep001.readthedocs.io/en/master/

https://github.com/bids-bep001/bids-specification.

https://osf.io/k4bs5/

It is currently a work in progress but by far the best option at the moment for MP2RAGE data management.



## Python environment

More on this [here](https://the-turing-way.netlify.app/reproducible-research/renv/renv-package.html)

```bash
# create env
conda create --name crc_nighres python=3.7 

# activate it
conda activate crc_nighres

# deactivate it
conda deactivate

# export package list in the env into a YAML file
conda env export > environment.yml

# create env from YAML file
conda env create -f environment.yml

```

- [Conda cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)