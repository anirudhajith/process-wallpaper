# process-wallpaper

Python and shell scripts which sets the wallpaper to a wordcloud of the most resource-intensive processes currently running.

![](https://raw.githubusercontent.com/anirudhajith/process-wallpaper/master/screenshot.png)

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

### Using a mask image for wordcloud
To create a masked wordcloud like:

![](https://github.com/zaphbbrox/process-wallpaper/raw/kde_devel/wc.png)

You'll have to put an image inside the app directory and edit the mask value in `config.json` to the name of that file. 

## Use
The wallpaper is updated every time `updateWallpaper.sh` is run. To trigger the update every minute, append the following line to `crontab -e`:
```
* * * * * /path/to/script/directory/updateWallpaper.sh

```
