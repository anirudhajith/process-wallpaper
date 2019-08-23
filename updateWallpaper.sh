#!/bin/bash
if [[ "$OSTYPE" =~ ^msys ]]; then
  ## Fixes the installer on Bash for Windows
  nice py -3 generateWallpaper.py
else
  nice python3 generateWallpaper.py
fi

#export DISPLAY=:1
