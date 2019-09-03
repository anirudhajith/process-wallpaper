#!/bin/bash

echo "Creating wallpaper..."
#export DISPLAY=:1
top -b -n 1 > top.out
nice python3 generateWallpaper.py

sh setWallpaper.sh