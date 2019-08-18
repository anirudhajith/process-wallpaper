PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/anirudh/Android/Sdk/emulator:/home/anirudh/Android/Sdk/tools:/home/anirudh/Android/Sdk/tools/bin:/home/anirudh/Android/Sdk/platform-tools:/home/anirudh/ReactNative/node_modules/.bin

top -b -n 1 > top.out
python3 generateWallpaper.py
WALLPAPER_PATH="file://$(pwd)/wallpaper.png"
gsettings set org.gnome.desktop.background picture-uri $WALLPAPER_PATH