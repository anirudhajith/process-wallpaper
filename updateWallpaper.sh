#!/bin/bash

#export DISPLAY=:1
top -b -n 1 > top.out
nice python3 generateWallpaper.py
