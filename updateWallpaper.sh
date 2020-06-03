#!/bin/bash

# Usual path where 'top', 'python3', 'gsettings' etc., reside
PATH=$PATH:/usr/bin

# Get the full directory name of the script no matter where it is being called from
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Save top's output to our app directory
top -b -n 1 -i -w 512 > $APP_DIR/top.out

# This is important!
cd $APP_DIR

python3 $APP_DIR/generateWallpaper.py

# Using the same picture twice so KDE Plasma actually changes the wallpaper in 
# slideshow mode, since apparently Plasma doesn't recognize the changes in 
# standard mode
cp wallpaper_new.png wallpaper.png
