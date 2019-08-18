import re
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS 


commandList = []

with open("top.txt", "r") as topFile:
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

print(resourceDict)

wc = WordCloud(background_color="black",width=1920,height=1080,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(resourceDict)
wc.to_file('wc.png')