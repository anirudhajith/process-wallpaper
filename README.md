# process-wallpaper

Python and shell scripts which set your wallpaper to a wordcloud of the most resource-intensive processes presently running.

![](https://raw.githubusercontent.com/anirudhajith/process-wallpaper/master/screenshot.png)

## Dependencies
* `python3`
* `gsettings` (comes preinstalled with GNOME) or `feh` (supported by many Linux distributions). 

If neither `gsettings` not `feh` are supported by your platform, you can still set `wallpaper.png` as your wallpaper manually.

## Setup

* Clone this repo.

```
git clone https://github.com/anirudhajith/process-wallpaper.git
```

* Set the resolution of your display in `config.json`
* Install Python dependencies.
```
pip3 install -r requirements.txt --user
```

## Usage

The wallpaper is updated every time `updateWallpaper.sh` is run. To trigger the update every minute, append the following line to `crontab -e`:
```
* * * * * cd /path/to/script/directory && ./updateWallpaper.sh > /tmp/wallpaper.log 2>&1
```

### CLI

`genWallpaper.py` can also be used as a CLI utility.

```
$ python3 genWallpaper.py --help
```
```
Usage: generateWallpaper.py [OPTIONS]

Options:
  -r, --resolution INTEGER...  The resolution (width, height) of the wallpaper
                               to generate.
  -bg, --bgcolor TEXT          Background color.
  -m, --margins INTEGER...     The margins (horizontal, vertical) around the
                               outside of the text, in pixels.
  -o, --output FILENAME        Where to output the wallpaper.  [default:
                               wallpaper.png]
  --config FILENAME            Path of the config file. Options are overridden
                               by command line arguments.  [default:
                               config.json]
  --help                       Show this message and exit.
```