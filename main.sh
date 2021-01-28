#!/bin/bash
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

#install MoviePY
pip install MoviePy


#SCRIPT_PATH=$(dirname $(realpath -s $0))"/Project_Starter-Baguette-master/"
#PATH=$PATH:$SCRIPT_PATH
#export PATH

python main.py

ffplay ./output/bar_chart_race.mp4
