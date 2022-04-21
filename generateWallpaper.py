import re
from PIL import Image
from wordcloud import WordCloud
import json
import os

commandList = []

with open("top.out", "r") as topFile:
    topOutput = topFile.read().split("\n")[7:]

    for line in topOutput[:-1]:
        line = re.sub(r'\s+', ' ', line).strip()
        fields = line.split(" ")

        try:
            if fields[11].count("/") > 0:
                command = fields[11].split("/")[0]
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

configJSON = json.loads(open("config.json", "r").read())

width, height = None, None
try:
    width = configJSON['resolution']['width']
    height = configJSON['resolution']['height']
except:
    pass

# if width or height were not found in the config try to get it from the system
# WARNING: this does not work properly for multi monitor setups
if not width or not height:
    try:
        width, height = ((os.popen("xrandr | grep '*'").read()).split()[0]).split("x")
        width = int(width)
        height = int(height)
    except:
        pass

# for full API see
# https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html
wc = WordCloud(
    background_color=configJSON["wordcloud"]["background"],
    width=width - 2 * int(configJSON["wordcloud"]["margin"]),
    height=height - 2 * int(configJSON["wordcloud"]["margin"]),
    margin=configJSON["wordcloud"]["margin"]
).generate_from_frequencies(resourceDict)

wc.to_file('wallpaper.png')

