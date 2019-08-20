#!/bin/bash
WALLPAPER_PATH="$(pwd)/wallpaper.png"


if command -v feh
then
  feh --bg-fill $WALLPAPER_PATH
elif command -v gsettings
then
  gsettings set org.gnome.desktop.background picture-uri "file://$WALLPAPER_PATH"
else
  echo "Don't know how to set wallpaper on your system. You need to manually set your wallpaper to ${WALLPAPER_PATH} ."
fi

