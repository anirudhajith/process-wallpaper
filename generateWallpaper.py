import re
from PIL import Image
from wordcloud import WordCloud
import numpy as np
import json

commandList = []

with open("top.out", "r") as topFile:
    topOutput = topFile.read().split("\n")[7:]
    
    for line in topOutput[:-1]:
        line = re.sub(r'\s+', ' ', line).strip()
        fields = line.split(" ")
        
        if fields[11].count("/") > 0:
            command = fields[11].split("/")[0]
        else:
            command = fields[11]
        
        cpu = float(fields[8])
        mem = float(fields[9])

        commandList.append((command, cpu, mem))
    

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

wc = WordCloud(
    background_color = configJSON["wordcloud"]["background"],
    width = int(configJSON["resolution"]["width"] * (1 - configJSON["wordcloud"]["margin"])),
    height = int(configJSON["resolution"]["height"] * (1 - configJSON["wordcloud"]["margin"]))
).generate_from_frequencies(resourceDict)

wc.to_file('wc.png')

wordcloud = Image.open("wc.png")
wallpaper = Image.new('RGB', (configJSON["resolution"]["width"], configJSON["resolution"]["height"]), configJSON["wordcloud"]["background"])
wallpaper.paste(
    wordcloud, 
    (
        int(configJSON["resolution"]["width"] * configJSON["wordcloud"]["margin"] / 2), 
        int(configJSON["resolution"]["height"] * configJSON["wordcloud"]["margin"] / 2)
    )    
)
wallpaper.save("wallpaper.png")
