#!/usr/bin/env python
import re
import psutil
import json
import os
from sys import platform
from PIL import Image
from wordcloud import WordCloud



def init_screen_sizes(configJSON):
    width, height = None, None
    if platform == "linux" or platform == "linux2":
        try:
            width, height = (
                (os.popen("xrandr | grep '*'").read()).split()[0]).split("x")
        except:
            pass
    elif platform == "darwin":
        try:
            results = str(subprocess.Popen(
                ['system_profiler SPDisplaysDataType'], stdout=subprocess.PIPE, shell=True).communicate()[0])
            res = re.search('Resolution: \d* x \d*',
                            results).group(0).split(' ')
            width, height = res[1], res[3]
        except:
            pass
    else:
        width = int(configJSON["resolution"]["width"])
        height = int(configJSON["resolution"]["height"])

    return (width, height)

def borderize(width, height, margin, background):
    cloud = Image.open("wallpaper.png")
    wallpaper = Image.new(
        'RGB',
        (width, height),
        background
    )
    wallpaper.paste(cloud, (margin, margin))
    wallpaper.save("wallpaper.png")

def get_resources():
    resourceDict = dict()
    for proc in psutil.process_iter(attrs=['name', 'cpu_percent', 'memory_percent']):
        try:
            if os.name != 'nt':
                name = proc.name()
            else:
                executable = proc.name()
                name, extension = os.path.splitext(executable)
            if name != "Python":
                relevancy = (proc.cpu_percent() ** 2 +
                             proc.memory_percent() ** 2) ** 0.5
                if name in resourceDict:
                    resourceDict[name] = resourceDict[name] + relevancy
                else:
                    resourceDict[name] = relevancy
        except:
            pass
    return resourceDict

def dump_screen_sizes(configJSON, screen_sizes):
    width = screen_sizes[0]
    height = screen_sizes[1]
    if height and width:
        configJSON["resolution"]["width"] = int(width)
        configJSON["resolution"]["height"] = int(height)
        with open('config.json', 'w') as f:
            json.dump(configJSON, f, indent=4)



configJSON = json.loads(open("config.json", "r").read())
margin = int(configJSON["wordcloud"]["margin"])
background = configJSON["wordcloud"]["background"]

screen_sizes = init_screen_sizes(configJSON)
dump_screen_sizes(configJSON, screen_sizes)

resourceDict = get_resources()

width = screen_sizes[0]
height = screen_sizes[1]
cloud = WordCloud(
    background_color=background,
    width=int(width - (2 * margin)),
    height=int(height - (2 * margin))
).generate_from_frequencies(resourceDict)
cloud.to_file("wallpaper.png")

borderize(width, height, margin, background)
