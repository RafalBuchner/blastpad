# !/bin/bash

# create blastPadEnv
echo "installing python virtual env for BlastPad"
python3 -m venv ${PWD}/venv
source ${PWD}/venv/bin/activate

echo "\n\ninstalling nescessary packages\n\n"

pip install --upgrade pip
pip3 install PyQt5
pip3 install PyInstaller