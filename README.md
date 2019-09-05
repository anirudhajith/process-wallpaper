# process-wallpaper

Python and shell scripts which set your wallpaper to a wordcloud of the most resource-intensive processes presently running.

![](https://raw.githubusercontent.com/anirudhajith/process-wallpaper/master/screenshot.png)

## Depenendencies
* `python3`
* `gsettings` (comes preinstalled with GNOME) or `feh` (supported by many Linux distributions). 

If neither `gsettings` not `feh` are supported by your platform, you can still set `wallpaper.png` as your wallpaper manually.

## Setup

* Clone this repo.

```
git clone https://github.com/anirudhajith/process-wallpaper.git
cd process-wallpaper
```
* Set the resolution of your display in `config.json`
* Install Python dependencies.
```
pip3 install -r requirements.txt --user
```
* Run `setup.sh`
```
./setup.sh
```

## Use
The wallpaper is updated every time `updateWallpaper.sh` is run. To trigger the update every minute, append the following line to `crontab -e`, remember to replace `/path/to/script/directory` with the directory of your scripts.
### KDE
```
* * * * * export "binpath=/path/to/script/directory"; "DISPLAY=:$(ls -1 /tmp/.X11-unix/X* | grep -oE "[0-9]*$" | sort -n | head -1)"; export "DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus"; (pushd "${binpath}" && ./updateWallpaper.sh && ./setWallpaper.sh; popd) 2>&1 | logger -t "process-wallpaper"
```
### Most other
```
* * * * * cd /path/to/script/directory && ./updateWallpaper.sh > /tmp/wallpaper.log 2>&1

```
