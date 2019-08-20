#!/bin/bash

# Usual path where 'top', 'python3', 'gsettings' etc., reside
PATH=$PATH:/usr/bin

# Get the full directory name of the script no matter where it is being called from
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Save top's output to our app directory
top -b -n 1 > $APP_DIR/top.out

# This is important!
cd $APP_DIR

python3 $APP_DIR/generateWallpaper.py

WALLPAPER_PATH="file://${APP_DIR}/wallpaper.png"
gsettings set org.gnome.desktop.background picture-uri $WALLPAPER_PATH