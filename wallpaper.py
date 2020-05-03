import os
import sys
import random
import subprocess
import datetime
import time
import logging

from middleware import Middleware, TimeDateBox, WeatherBox

from PIL import Image, ImageFont, ImageDraw

RENDEREDIMAGE = "/tmp/wallpaper.png"
WALLDIR = "/home/realloc/wallpapers"
FONT = "./font.ttf"
SLEEP = "30"
LOGFILE = "/tmp/wallpaper.log"

logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)


def set_background(path: str):
    args = ["feh", "--bg-center", path]
    result = subprocess.run(args, capture_output=True)  # blocking
    if result.returncode == 0:
        logging.info("Successfully set wallpaper")
        return
    else:
        logging.error("Error setting wallpaper!")
        logging.error("subprocess command: " + result.args)
        logging.error("stdout: " + result.stdout)
        logging.error("stderr: " + result.stderr)
        return


def modify_image(image: Image, middleware: [Middleware]):
    """ convert to appropriate resolution and format """
    draw = ImageDraw.Draw(im)

    for m in middleware:
        m.draw(draw)


class WallpaperPicker(object):
    """ Pick a wallpaper from dir """

    def __init__(self, directory):
        # Build a list of abs paths of wallpapers in directory
        self.directory = directory
        self.wallpapers = []
        for (dirpath, _folders, files) in os.walk(directory):
            for file in files:
                abspath = os.path.join(dirpath, file)
                self.wallpapers.append(abspath)

        if not self.wallpapers:
            msg = f"No wallpapers found ({self.directory}). See log file {LOGFILE} for more info"
            logging.warn(msg + " .Quitting!")
            print(msg)
            sys.exit(1)

    def pickRandom(self) -> str:
        chosen = random.choice(self.wallpapers)
        return chosen


if __name__ == '__main__':
    picker = WallpaperPicker(WALLDIR)

    middleware = [
        WeatherBox(50, 10),
        TimeDateBox(50, 50),
    ]

    cache: [(str, Image)] = []  # [(name, Image)]

    while True:
        chosen = picker.pickRandom()
        logging.info("Choosing wallpaper...: " + chosen)

        im: Image = None  # copy

        # check if chosen image is in cache
        for name, cached_image in cache:
            if name == chosen:
                logging.info("Loaded it from cache")
                im = cached_image.copy()
                # print("Colors:", cached_image.getcolors())
                break
        else:
            logging.info("Not found in cache. Adding it to cache")
            new_image: Image = Image.open(chosen).resize((1920, 1080))
            cache.append((chosen, new_image))
            im = new_image.copy()

        modify_image(im, middleware)
        im.save(RENDEREDIMAGE)

        logging.info("Writing image to: " + RENDEREDIMAGE)

        set_background(RENDEREDIMAGE)
        time.sleep(5)
