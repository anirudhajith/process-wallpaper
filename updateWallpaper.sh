top -b -n 1 > top.out
python3 generateWallpaper.py
WALLPAPER_PATH="file://$(pwd)/wallpaper.png"
gsettings set org.gnome.desktop.background picture-uri $WALLPAPER_PATH