# Download version 6 through https://services.healthtech.dtu.dk/services/SignalP-6.0/

# tar -xzf signalp-6.0i.slow_sequential.tar.gz
# pip install -r requirements.txt
# pip install signalp6_slow_sequential/signalp-6-package/
# pip install "numpy<2"

## Because signal p only operates with python 3.10, and I had 3.12, 
## I had to activate a conda environmnet with version 3.10

# Download miniconda to get conda inside the server:
# cd ~
# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# bash Miniconda3-latest-Linux-x86_64.sh

# export PATH="$HOME/miniconda3/bin:$PATH"
# conda create -n signalp310 python=3.10
# source "$HOME/miniconda3/bin/activate" signalp310 to activate the python 3.10 environment. 
# python --version

## To activate everytime:
# export PATH="$HOME/miniconda3/bin:$PATH" 
# source "$HOME/miniconda3/bin/activate" signalp310

# Need to change to Python 3.9
# source "$HOME/miniconda3/bin/activate" signalp39

## Installing the signal-p package 
# cd ~/07_fold_all/signalp6_slow_sequential/signalp-6-package
# python -m pip install .

