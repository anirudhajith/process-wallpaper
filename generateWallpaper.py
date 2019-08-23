#!/usr/bin/env python
import re
import psutil
import json
import os
from sys import platform
from PIL import Image
from wordcloud import WordCloud

resourceDict = dict()

for proc in psutil.process_iter(attrs=['name', 'cpu_percent', 'memory_percent']):
    try:
        name = proc.name()
        if name != "Python":
            relevancy = (proc.cpu_percent() ** 2 + proc.memory_percent() ** 2) ** 0.5
            if name in resourceDict:
                resourceDict[name] = resourceDict[name] + relevancy
            else:
                resourceDict[name] = relevancy
    except:
        pass

width, height = None, None

if platform == "linux" or platform == "linux2":
    try:
        width,height = ((os.popen("xrandr | grep '*'").read()).split()[0]).split("x")
    except:
        pass
elif platform == "darwin":
    try:
        results = str(subprocess.Popen(['system_profiler SPDisplaysDataType'],stdout=subprocess.PIPE, shell=True).communicate()[0])
        res = re.search('Resolution: \d* x \d*', results).group(0).split(' ')
        width, height = res[1], res[3]
    except:
        pass

configJSON = json.loads(open("config.json", "r").read())

if height and width:
    configJSON["resolution"]["width"] = int(width)
    configJSON["resolution"]["height"] = int(height)
    with open('config.json', 'w') as f:
        json.dump(configJSON, f, indent=4)

cloud = WordCloud(
    background_color = configJSON["wordcloud"]["background"],
    width = int(configJSON["resolution"]["width"] - 2 * configJSON["wordcloud"]["margin"]),
    height = int(configJSON["resolution"]["height"] - 2 * configJSON["wordcloud"]["margin"])
).generate_from_frequencies(resourceDict)

cloud.to_file("wallpaper.png")
wallpaper = Image.open("wallpaper.png")
wallpaper = Image.new('RGB', (configJSON["resolution"]["width"], configJSON["resolution"]["height"]), configJSON["wordcloud"]["background"])
wallpaper.paste(cloud, None)
wallpaper.save("wallpaper.png")
