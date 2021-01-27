#!/bin/bash
#install get geoscripting environment
git clone https://github.com/GeoScripting-WUR/InstallLinuxScript.git
cd InstallLinuxScript/user
chmod u+x ./install.sh
./install.sh

cd

#install ffmpeg
sudo apt update
sudo apt install ffmpeg

#activate geoscripting environment
source activate geoscripting
which pip

#install bar_chart_race
pip install bar_chart_race

#install image.io
pip install imageio




