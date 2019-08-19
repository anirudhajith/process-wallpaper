#!/bin/bash

echo "Installing Python dependencies..."
pip3 install --user Pillow
pip3 install --user wordcloud
pip3 install --user matplotlib

WALLPAPER_PATH="file://$(pwd)/wallpaper.png"
chmod +x updateWallpaper.sh

echo "Creating wallpaper..."
./updateWallpaper.sh

echo "Setting wallpaper..."
gsettings set org.gnome.desktop.background picture-uri $WALLPAPER_PATH

echo "Setup successfully completed"
