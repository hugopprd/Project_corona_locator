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

#install selenium
pip install -U selenium

#install geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver

#install cutycapt
sudo apt-get install -y cutycapt

cd




