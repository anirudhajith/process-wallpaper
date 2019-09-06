import json
import os
import time
from collections import defaultdict

import psutil
from PIL import Image
from wordcloud import WordCloud

# get all process names with cpu and memory usage
all_processes = defaultdict(lambda: {'cpu_percent': 0, 'memory_percent': 0})

# cpu_percent only reports the cpu since the last time it was run, and always returns 0% usage on first run
[proc.as_dict() for proc in psutil.process_iter()]
time.sleep(0.2)  # wait so that we're not measuring cpu/memory usage of the time between process_iter calls.

for proc in psutil.process_iter():
    details = proc.as_dict(attrs=['name', 'cpu_percent', 'memory_percent'])

    name = details['name'].split("/")[0]
    all_processes[name]['cpu_percent'] += details['cpu_percent'] or 0
    all_processes[name]['memory_percent'] += details['memory_percent'] or 0

# generate a single real number metric for resource-intensity
frequencies = {}

for name, resources in all_processes.items():
    frequencies[name] = (resources['cpu_percent'] ** 2 + resources['memory_percent'] ** 2 + 1) ** 0.5

# create wallpaper
width, height = None, None
try:
    width, height = ((os.popen("xrandr | grep '*'").read()).split()[0]).split("x")
    width = int(width)
    height = int(height)
except:
    pass

config = json.loads(open("config.json", "r").read())

if not width or not height:
    width = config['resolution']['width']
    height = config['resolution']['height']

wc = WordCloud(
    background_color=config["wordcloud"]["background"],
    width=width - 2 * int(config["wordcloud"]["margin"]),
    height=height - 2 * int(config["wordcloud"]["margin"])
).generate_from_frequencies(frequencies)

wc.to_file('wc.png')

wordcloud = Image.open("wc.png")
wallpaper = Image.new('RGB', (width, height), config["wordcloud"]["background"])
wallpaper.paste(
    wordcloud,
    (
        config["wordcloud"]["margin"],
        config["wordcloud"]["margin"]
    )
)
wallpaper.save("wallpaper.png")
