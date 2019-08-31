import json
import os
import re
from typing import Tuple, BinaryIO, TextIO

import click
from PIL import Image, ImageColor
from wordcloud import WordCloud


def get_freqs():
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

    return resourceDict


def validate_color(ctx, param, value):
    try:
        return ImageColor.getrgb(value)
    except ValueError:
        raise click.BadParameter('Colors should be CSS3-like strings, e.g. #101010 or rgb(123, 123, 123).')


@click.command()
@click.option(
    '--resolution', '-r',
    help='The resolution (width, height) of the wallpaper to generate.',
    type=(int, int)
)
@click.option(
    '--bgcolor', '-bg',
    help='Background color.'
)
@click.option(
    '--margins', '-m',
    help='The margins (horizontal, vertical) around the outside of the text, in pixels.',
    type=(int, int)
)
@click.option(
    '--output', '-o',
    help='Where to output the wallpaper.',
    type=click.File('wb'),
    default='wallpaper.png',
    show_default=True
)
@click.option(
    '--config',
    help='Path of the config file. Options are overridden by command line arguments.',
    type=click.File('r'),
    default='config.json',
    show_default=True
)
def main(resolution: Tuple[int, int], bgcolor, margins: Tuple[int, int], output: BinaryIO, config: TextIO):
    if config:
        config = json.load(config)

    frequencies = get_freqs()

    if not resolution:
        width, height = None, None
        try:
            width, height = ((os.popen("xrandr | grep '*'").read()).split()[0]).split("x")
            width = int(width)
            height = int(height)
        except:
            pass

        if not width or not height:
            width = config['resolution']['width']
            height = config['resolution']['height']
    else:
        width, height = resolution

    if margins:
        horiz_margin, vert_margin = margins
    else:
        horiz_margin = int(config['wordcloud']['margin'])
        vert_margin = int(config['wordcloud']['margin'])
    wc = WordCloud(
        background_color=bgcolor or config["wordcloud"]["background"],
        width=width - 2 * horiz_margin,
        height=height - 2 * vert_margin
    ).generate_from_frequencies(frequencies)

    wc.to_file('wc.png')

    wordcloud = Image.open("wc.png")
    wallpaper = Image.new('RGB', (width, height), bgcolor or config["wordcloud"]["background"])
    wallpaper.paste(
        wordcloud,
        margins or (config["wordcloud"]["margin"], config["wordcloud"]["margin"])
    )

    wallpaper.save(output)


if __name__ == '__main__':
    main()
