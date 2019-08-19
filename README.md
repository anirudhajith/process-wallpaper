# process-wallpaper

Python and shell scripts which sets the wallpaper to a wordcloud of the most resource-intensive processes currently running.

![](https://raw.githubusercontent.com/anirudhajith/process-wallpaper/master/wallpaper.png)

## Depenendencies
* `python3`
* A GNOME desktop environment is required for `setup.sh` to change the wallpaper automatically. Alternatively, you may set `wallpaper.png` as your wallpaper manually.

## Setup
* Set the resolution of your display in `config.json`
* Use the following commands
```
cd /path/to/script/directory
chmod +x setup.sh
./setup.sh
```

## Use
The wallpaper is updated every time `updateWallpaper.sh` is run. To trigger the update every minute, append the following line to `crontab -e`:
```
* * * * * cd /path/to/script/directory && ./updateWallpaper.sh > /tmp/wallpaper.log 2>&1

```