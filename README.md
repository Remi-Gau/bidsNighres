# CRC nighres

For processing of high-res images from the 
[CRC](https://www.campus.uliege.be/cms/c_1841124/fr/b30-centre-de-recherches-du-cyclotron-crc) 
using [nighres](https://nighres.readthedocs.io/en/latest/).

### virtualenv

```bash
# create a new virtual environment in crc_nighres
$ virtualenv --python=python3 crc_nighres
# activate the new environment
$ source crc_nighres/bin/activate
```

## Installation

Nighres is already part of this repo as a submodule added like this.

```
cd lib
git submodule add https://github.com/nighres/nighres.git
```

### Install Nighres

See [here](https://nighres.readthedocs.io/en/latest/installation.html).

#### Set up java

```bash
sudo apt-get install openjdk-8-jdk
export JCC_JDK=/usr/lib/jvm/java-8-openjdk-amd64
python3 -m pip install jcc
```
#### Install java

```bash
cd lib/nighres
./build.sh
python3 -m pip install .
```

## Data structure

Assumes a BIDS.

More specifically the one described by the BEP-001 of BIDS

- https://bep001.readthedocs.io/en/master/

- https://github.com/bids-bep001/bids-specification.

- https://osf.io/k4bs5/

It is currently a work in progress but by far the best option at the moment 
for MP2RAGE data management.
