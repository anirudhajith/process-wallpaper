#!/bin/bash

echo "Installing Python dependencies..."
pip3 install --user Pillow wordcloud matplotlib

echo "Creating wallpaper..."
sh updateWallpaper.sh

echo "Setting wallpaper..."
sh setWallpaper.sh

echo "Setup successfully completed"
