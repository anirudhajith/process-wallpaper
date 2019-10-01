import re
from PIL import Image
from wordcloud import WordCloud
import json
import os
from matplotlib.colors import LinearSegmentedColormap
import random

colors = [
    [
        '#022f40',#RICH BLACK
        '#38aecc',#MAXIMUM BLUE
        '#0090c1',#BLUE (NCS)
        '#183446',#YANKEES BLUE
        '#046e8f',#SEA BLUE
    ],
    [
        '#041b15',#RICH BLACK (FOGRA29)
        '#136f63',#DEEP GREEN-CYAN TURQUOISE
        '#22aaa1',#LIGHT SEA GREEN
        '#4ce0d2',#TURQUOISE
        '#84cae7',#SKY BLUE
    ],
    [
        '#f433ab',#FROSTBITE
        '#cb04a5',#DEEP MAGENTA
        '#934683',#PLUM
        '#65334d',#WINE DREGS
        '#2d1115',#DARK SIENNA
    ],
    [
        '#4f000b',#BULGARIAN ROSE
        '#720026',#BURGUNDY
        '#ce4257',#BRICK RED
        '#ff7f51',#CORAL
        '#ff9b54',#PINK-ORANGE
    ],
    [
        '#f2dc5d',#STIL DE GRAIN YELLOW
        '#f2db59',#MUSTARD
        '#dbc964',#BOOGER BUSTER
        '#a38b03',#DARK YELLOW
        '#352f0a',#PULLMAN GREEN
    ],
    [
        '#6e44ff',#VERY LIGHT BLUE
        '#a991ff',#PALE VIOLET
        '#cfc1ff',#PERIWINKLE
        '#a78eff',#PALE VIOLET
        '#937aef',#MEDIUM PURPLE
    ],
    [
        '#8b1e3f',#BIG DIP O’RUBY
        '#3d1521',#DARK SIENNA
        '#bc8797',#ENGLISH LAVENDER
        '#ef86a5',#VANILLA ICE
        '#db3f6e',#PARADISE PINK
    ],
    [
        '#3d3522',#OLIVE DRAB (#7)
        '#49412d',#TAUPE
        '#605438',#UMBER
        '#af9557',#DEER
        '#f7e9ca',#CHAMPAGNE
    ],
    [
        '#424342',#ARSENIC
        '#244f24',#CAL POLY POMONA GREEN
        '#1b6d1b',#LINCOLN GREEN
        '#109910',#INDIA GREEN
        '#1efc1e',#NEON GREEN
    ],
    [
        '#595959',#DAVY'S GREY
        '#7f7f7f',#TROLLEY GREY
        '#a5a5a5',#QUICK SILVER
        '#cccccc',#PASTEL GRAY
        '#f2f2f2',#ANTI-FLASH WHITE
    ],
    [
        '#274060',#JAPANESE INDIGO
        '#345582',#B'DAZZLED BLUE
        '#66a8ff',#FRENCH SKY BLUE
        '#1a2d44',#YANKEES BLUE
        '#5894e2',#UNITED NATIONS BLUE
    ],
    [
        '#0c0a3e',#MIDDLE RED PURPLE
        '#201d7a',#ST. PATRICK'S BLUE
        '#423eb2',#OCEAN BLUE
        '#554ff9',#MAJORELLE BLUE
        '#7a76f2',#MEDIUM SLATE BLUE
    ],
    [
        '#650d1b',#DARK SCARLET
        '#820015',#RED DEVIL
        '#9b1229',#RUBY RED
        '#ad1b34',#VIVID BURGUNDY
        '#dd1f3e',#CRIMSON
    ],
    [
        '#0d0221',#RICH BLACK (FOGRA29)
        '#1f0849',#MIDDLE RED PURPLE
        '#49258c',#KSU PURPLE
        '#b7a7d6',#LIGHT PASTEL PURPLE
        '#cfc2e8',#SOAP
    ],
    [
        '#af3800',#MAHOGANY
        '#ff631c',#GIANTS ORANGE
        '#fc4f00',#INTERNATIONAL ORANGE (AEROSPACE)
        '#ce4100',#SINOPIA
        '#ff5000',#INTERNATIONAL ORANGE
    ],
    [
        '#ecba82',#PALE GOLD
        '#e28e2d',#CADMIUM ORANGE
        '#f4b56e',#MELLOW APRICOT
        '#f7f0e8',#LINEN
        '#c19a6e',#WOOD BROWN
    ],
    [
        '#f6fedb',#BEIGE
        '#d5e5a2',#PALE GOLDENROD
        '#c1d875',#MEDIUM SPRING BUD
        '#aac454',#MONOCHROMATIC MODE
        '#7d962a',#OLIVE DRAB (#3)
    ]
]
colorMap = LinearSegmentedColormap.from_list("mycmap", colors[random.randint(1,len(colors))])
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
    height=height - 2 * int(configJSON["wordcloud"]["margin"]),
    colormap=colorMap
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
