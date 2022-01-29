- [bidsNighres](#bidsnighres)
    - [Installation](#installation)
        - [Install Nighres](#install-nighres)
            - [Set up java](#set-up-java)
            - [Install java](#install-java)
    - [Running the app](#running-the-app)

# bidsNighres

BIDS app to help preprocessing high-res anatomical data using
[nighres](https://nighres.readthedocs.io/en/latest/).

<!-- TODO seems hard to install JDK, nighres in virtual environment

### virtualenv

```bash
# create a new virtual environment in crc_nighres
$ virtualenv --python=python3 crc_nighres
# activate the new environment
$ source crc_nighres/bin/activate
```
-->

## Installation

Nighres is already part of this repo as a submodule added like this.

```
cd lib
git submodule add https://github.com/nighres/nighres.git
```

### Install Nighres

See [here](https://nighres.readthedocs.io/en/latest/installation.html).

Summary below!

#### Set up java

```bash
sudo apt-get install openjdk-8-jdk
export JCC_JDK=/usr/lib/jvm/java-8-openjdk-amd64

# this may fail when in a virtual environment
python3 -m pip install jcc
```

#### Install java

```bash
cd lib/nighres
./build.sh
python3 -m pip install .
```

<!--
### Docker

```
docker run --rm \
-v /home/remi/gin/V5_high-res/pilot_1:/data \
-p 8888:8888 nighres
```

Running this might require to kill some process (java) that uses the 8888 port.

```
docker rm -fv $(docker ps -aq)  # Remove all containers
sudo lsof -i -P -n | grep <port number>  # List who's using the port
sudo kill <process id>
```

https://stackoverflow.com/questions/37971961/docker-error-bind-address-already-in-use
-->

## Running the app

```bash

root_dataset=${PWD}/../../..

input_dataset=${root_dataset}/inputs/raw/
output_location=${root_dataset}/derivatives/bidsNighres/

filter_file=${root_dataset}/code/filter_file.json

echo ${input_dataset}

python run.py --input-datasets ${input_dataset} \
              --output-location ${output_location} \
              --analysis-level participant \
              --participant-label pilot001 \
              --action skullstrip \
              --bids-filter-file ${filter_file}
```
