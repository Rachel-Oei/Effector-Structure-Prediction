#!/bin/bash

# Download version 6 through https://services.healthtech.dtu.dk/services/SignalP-6.0/

# tar -xzf signalp-6.0i.slow_sequential.tar.gz
# pip install -r requirements.txt
# pip install signalp6_slow_sequential/signalp-6-package/
# pip install "numpy<2"

## Because signal p only operates with python 3.10, and I had 3.12, 
## I had to activate a conda environmnet with version 3.9

# Download miniconda to get conda inside the server:
# cd ~
# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# bash Miniconda3-latest-Linux-x86_64.sh

# export PATH="$HOME/miniconda3/bin:$PATH"
# conda create -n signalp310 python=3.9

## To activate everytime:
# export PATH="$HOME/miniconda3/bin:$PATH" 
# source "$HOME/miniconda3/bin/activate" signalp39

## Installing the signal-p package 
# cd ~/07_fold_all/signalp6_slow_sequential/signalp-6-package
# python -m pip install .

# Fungi are eukaryotic organisms, short output with no graphics, slow prediction mode. 

signalp6 \
    --model_dir "/home/rachel/07_fold_all/signalp6_slow_sequential/signalp-6-package/models/" \
    --ff $all_aa_dir \
    --org eukarya \
    --od $out_dir \
    --fmt txt \
    --mode slow-sequential