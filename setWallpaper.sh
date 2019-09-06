#!/bin/bash
WALLPAPER_PATH="$(pwd)/wallpaper.png"


if pgrep plasmashell >/dev/null; then
  qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "var allDesktops = desktops();print (allDesktops);for (i=0;i<allDesktops.length;i++) {d = allDesktops[i];d.wallpaperPlugin = 'org.kde.image';d.currentConfigGroup = Array('Wallpaper', 'org.kde.image', 'General');d.writeConfig('Image', 'file://$(dirname ${WALLPAPER_PATH})/wc.png')}"
  qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "var allDesktops = desktops();print (allDesktops);for (i=0;i<allDesktops.length;i++) {d = allDesktops[i];d.wallpaperPlugin = 'org.kde.image';d.currentConfigGroup = Array('Wallpaper', 'org.kde.image', 'General');d.writeConfig('Image', 'file://${WALLPAPER_PATH}')}"
elif command -v gsettings
then
  gsettings set org.gnome.desktop.background picture-uri "file://$WALLPAPER_PATH"
elif command -v feh
then
  feh --bg-fill $WALLPAPER_PATH
else
  echo "ERROR: Unable to automatically set wallpaper on your system. Manually set your wallpaper to ${WALLPAPER_PATH}."
fi

