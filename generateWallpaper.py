import re
import time
from collections import defaultdict

from PIL import Image
from wordcloud import WordCloud
import json
import os
import psutil

# get all process names with cpu and memory usage
all_processes = defaultdict(lambda: {'cpu_percent': 0, 'memory_percent': 0})

# cpu_percent only reports the cpu since the last time it was run, and always returns 0% usage on first run
[proc.as_dict() for proc in psutil.process_iter()]
time.sleep(0.2)  # wait so that we're not measuring cpu/memory usage of the time between process_iter calls.

for proc in psutil.process_iter():
    details = proc.as_dict(attrs=['name', 'cpu_percent', 'memory_percent'])
    
    if details['name'].count("/") > 0:
        details['name'] = details['name'].split("/")[0]
    
    if details['cpu_percent'] == None:
        details['cpu_percent'] = 0.0
    
    if details['memory_percent'] == None:
        details['memory_percent'] = 0.0
    
    if details['name'] not in all_processes:
        all_processes[details['name']] = details
    else:
        all_processes[details['name']]['memory_percent'] += details['memory_percent']
        all_processes[details['name']]['cpu_percent'] += details['cpu_percent']


# generate a single real number metric for resource-intensity
resourceDict = {}

for process_name in all_processes.keys():
    resourceDict[process_name] = (all_processes[process_name]['cpu_percent'] ** 2 + all_processes[process_name]['memory_percent'] ** 2 + 1) ** 0.5


# create wallpaper
width, height = None, None
try:
    width, height = ((os.popen("xrandr | grep '*'").read()).split()[0]).split("x")
    width = int(width)
    height = int(height)
except:
    pass

configJSON = json.loads(open("config.json", "r").read())

if not width or not height:
    width = configJSON['resolution']['width']
    height = configJSON['resolution']['height']

wc = WordCloud(
    background_color=configJSON["wordcloud"]["background"],
    width=width - 2 * int(configJSON["wordcloud"]["margin"]),
    height=height - 2 * int(configJSON["wordcloud"]["margin"])
).generate_from_frequencies(resourceDict)

wc.to_file('wc.png')

wordcloud = Image.open("wc.png")
wallpaper = Image.new('RGB', (width, height), configJSON["wordcloud"]["background"])
wallpaper.paste(
    wordcloud,
    (
        configJSON["wordcloud"]["margin"],
        configJSON["wordcloud"]["margin"]
    )
)
wallpaper.save("wallpaper.png")
