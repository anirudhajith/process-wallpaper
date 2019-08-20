import re
from PIL import Image
from wordcloud import WordCloud
import json
import locale

commandList = []
locale.setlocale(locale.LC_NUMERIC, '')

with open("top.out", "r") as topFile:
    topOutput = topFile.read().split("\n")[7:]
    
    for line in topOutput[:-1]:
        line = re.sub(r'\s+', ' ', line).strip()
        fields = line.split(" ")
        
        if fields[11].count("/") > 0:
            command = fields[11].split("/")[0]
        else:
            command = fields[11]
        
        cpu = 0
        mem = 0
        
        try:
            cpu = float(locale.atof(fields[8]))
        except ValueError:
            print("CPU usage parse error, tried values: " + fields[8])

        try:
            mem = float(locale.atof(fields[9]))
        except ValueError:
            print("Memory usage parse error, tried values: " + fields[9])

        if command != "top":
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
    width = int(configJSON["resolution"]["width"] - 2 * configJSON["wordcloud"]["margin"]),
    height = int(configJSON["resolution"]["height"] - 2 * configJSON["wordcloud"]["margin"])
).generate_from_frequencies(resourceDict)

wc.to_file('wc.png')

wordcloud = Image.open("wc.png")
wallpaper = Image.new('RGB', (configJSON["resolution"]["width"], configJSON["resolution"]["height"]), configJSON["wordcloud"]["background"])
wallpaper.paste(
    wordcloud, 
    (
        configJSON["wordcloud"]["margin"],
        configJSON["wordcloud"]["margin"]
    )    
)
wallpaper.save("wallpaper.png")
