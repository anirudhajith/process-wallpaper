#!/bin/bash

echo "Creating wallpaper..."

top -b -n 1 > top.out
nice python3 generateWallpaper.py

echo ""