import re
from os import path
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import os
import json
import os

configJSON = json.loads(open("config.json", "r").read())

# Check if image for mask exists, else don't use a mask for wordcloud
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
mask_img = configJSON["wordcloud"]["mask"]
print(mask_img)
if path.isfile(path.join(d, mask_img)):
    mask = np.array(Image.open(path.join(d, mask_img)))
else:
    mask = None

commandList = []

with open("top.out", "r") as topFile:
    topOutput = topFile.read().split("\n")[7:]

    for line in topOutput[:-1]:
        line = re.sub(r'\s+', ' ', line).strip()
        fields = line.split(" ")

        try:
            # added if, elif statement for KDE since some system processes are in brackets
            # and changed order how the commands are processed by these statements
            if fields[11].count("[") or fields[11].count("]") > 0:
                command = fields[11].strip('[]')
                if command.count("/") > 0:
                    command = command.split("/")[0]
            elif fields[11].count("/") > 0:
                command = fields[11].split("/")[-1]
            else:
                command = fields[11]

            cpu = float(fields[8].replace(",", "."))
            mem = float(fields[9].replace(",", "."))

            if command != "top":
                commandList.append((command, cpu, mem))
        except:
            pass       
           

commandDict = {}

for command, cpu, mem in commandList:
    if command in commandDict:
        commandDict[command][0] += cpu
        commandDict[command][1] += mem
    else:
        commandDict[command] = [cpu + 1, mem + 1]

resourceDict = {}

for command, [cpu, mem] in commandDict.items():
    resourceDict[command] = (cpu ** 2 + mem ** 2) ** 0.5

if not width or not height:
    width = configJSON['resolution']['width']
    height = configJSON['resolution']['height']

wc = WordCloud(
    background_color = configJSON["wordcloud"]["background"],
    width = int(configJSON["resolution"]["width"] - 2 * configJSON["wordcloud"]["margin"]),
    height = int(configJSON["resolution"]["height"] - 2 * configJSON["wordcloud"]["margin"]),
    # added mask switch for using an image for masking the wordcloud
    mask = mask 

).generate_from_frequencies(resourceDict)

# using different colormap with recolor function //since I like it more =)
wc.recolor(colormap="summer").to_file('wc.png')

wordcloud = Image.open("wc.png")
wallpaper = Image.new('RGB', (width, height), configJSON["wordcloud"]["background"])
wallpaper.paste(
    wordcloud,
    (
        configJSON["wordcloud"]["margin"],
        configJSON["wordcloud"]["margin"]
    )
)
# adding a second wallpaper for Plasma slideshow usage. See updateWalpaper.sh
wallpaper.save("wallpaper_new.png")