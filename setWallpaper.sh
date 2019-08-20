#!/bin/bash
WALLPAPER_PATH="$(pwd)/wallpaper.png"


if command -v gsettings
then
  gsettings set org.gnome.desktop.background picture-uri "file://$WALLPAPER_PATH"
elif command -v feh
then
  feh --bg-fill $WALLPAPER_PATH
else
  echo "ERROR: Unable to automatically set wallpaper on your system. Manually set your wallpaper to ${WALLPAPER_PATH}."
fi

