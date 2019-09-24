#!/bin/bash
WALLPAPER_PATH="$(pwd)/wallpaper.png"

echo "Setting wallpaper..."

if pgrep plasmashell >/dev/null; then
  qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "var allDesktops = desktops();print (allDesktops);for (i=0;i<allDesktops.length;i++) {d = allDesktops[i];d.wallpaperPlugin = 'org.kde.image';d.currentConfigGroup = Array('Wallpaper', 'org.kde.image', 'General');d.writeConfig('Image', 'file://$(dirname ${WALLPAPER_PATH})/wc.png')}"
  qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "var allDesktops = desktops();print (allDesktops);for (i=0;i<allDesktops.length;i++) {d = allDesktops[i];d.wallpaperPlugin = 'org.kde.image';d.currentConfigGroup = Array('Wallpaper', 'org.kde.image', 'General');d.writeConfig('Image', 'file://${WALLPAPER_PATH}')}"
  PLASMASHELL_WORKED=true
fi

if command -v gsettings > /tmp/wallpaper.log
then
  if [ $DESKTOP_SESSION == 'mate' ]
  then
    gsettings set org.mate.background picture-filename "$WALLPAPER_PATH"
  else
    gsettings set org.gnome.desktop.background picture-uri "file://$WALLPAPER_PATH"
  fi
  GSETTINGS_WORKED=true
fi

if command -v feh > /tmp/wallpaper.log
then
  feh --bg-fill $WALLPAPER_PATH
  FEH_WORKED=true
fi

if [ [ $PLASMASHELL_WORKED ] || [ $GSETTINGS_WORKED ] || [ $FEH_WORKED ] ]
then
  echo "Wallpaper set successfully"
else
  echo "[ERROR] Unable to automatically set wallpaper on your system. Please set wallpaper.png as your desktop wallpaper manually."
fi

echo ""