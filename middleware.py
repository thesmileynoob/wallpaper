# Middlewares
# A middleware draws arbitary stuff on the image passed to its draw() method.
# It should subclass Middleware of course


from PIL import Image, ImageFont, ImageDraw
import datetime
import urllib


class Middleware(object):

    DEFAULT_FONT_PATH: str = "./res/fonts/Pacifico-Regular.ttf"
    DEFAULT_FONT: ImageFont = ImageFont.truetype(DEFAULT_FONT_PATH, 28)

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self, draw: ImageDraw):
        pass


class TimeDateBox(Middleware):

    def draw(self, draw: ImageDraw):
        # date and time
        date_text = datetime.datetime.now().strftime("%A, %d of %B %Y")
        time_text = datetime.datetime.now().strftime("%H:%M:%S")

        xoff = self.x
        yoff = self.y
        font = self.DEFAULT_FONT

        # draw date
        _, line_height = font.getsize(date_text)
        draw.text((xoff, yoff), date_text, font=font)
        yoff += line_height / 1.5

        # draw time
        draw.text((xoff, yoff), time_text, font=font)


class WeatherBox(Middleware):

    def __init__(self, x, y):
        super().__init__(x,y)
        # TODO: fetch weather!
        self.weather= "Aurangabad: 32 °C"

    def draw(self, draw: ImageDraw):
        weather_text = self.weather

        xoff = self.x
        yoff = self.y
        font = self.DEFAULT_FONT

        draw.text((xoff, yoff), weather_text, font=font)
