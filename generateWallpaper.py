#!/usr/bin/env python
import re
import operator
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
            if name != "Python" or name != "System Idle Process" or name != "svchost":
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

def color_functions(dictionary = {}, mode = "default", color = "255,255,255"):
    most_recurrent = max(dictionary.items(), key=operator.itemgetter(1))

    def greyscale_by_frequency(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(0, 0%%, %d%%)" % (360 * dictionary[word])
    def singlecolor_by_frequency(word, font_size, position, orientation, random_state=None, **kwargs):
        def scale_number_over (original, frequency, max):
            decimal = dictionary[word] / most_recurrent[1]
            return (int(original) / 3) + (int(original) * decimal / (2 / 3))

        colors = color.split(',')
        r = scale_number_over(int(colors[0]), dictionary[word], most_recurrent[1])
        g = scale_number_over(
            int(colors[1]), dictionary[word], most_recurrent[1])
        b = scale_number_over(
            int(colors[2]), dictionary[word], most_recurrent[1])
        return "rgb(%d, %d, %d)" % (r, g, b)

    def apply_color(word, font_size, position, orientation, random_state=None, **kwargs):
        return "rgb(%s)" % (color)

    functions = {
        "greyscale": greyscale_by_frequency,
        "colorscale": singlecolor_by_frequency,
        "color": apply_color
    }

    return functions[mode]



configJSON = json.loads(open("config.json", "r").read())
margin = int(configJSON["wordcloud"]["margin"])
background = configJSON["wordcloud"]["background"]
mode = configJSON["wordcloud"]["mode"]
color = configJSON["wordcloud"]["color"]
repeating = configJSON["wordcloud"]["repeating"]

screen_sizes = init_screen_sizes(configJSON)
dump_screen_sizes(configJSON, screen_sizes)

resourceDict = get_resources()

width = screen_sizes[0]
height = screen_sizes[1]
cloud = WordCloud(
    background_color=background,
    width=int(width - (2 * margin)),
    height=int(height - (2 * margin)),
    color_func=None if mode == "default" else color_functions(
        resourceDict, mode, color
    ),
    repeat=repeating
).generate_from_frequencies(resourceDict)
cloud.to_file("wallpaper.png")

borderize(width, height, margin, background)
