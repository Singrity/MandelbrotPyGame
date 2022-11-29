from PIL import Image
import matplotlib.cm
import numpy as np
from mandelbrot import MandelbrotSet
#from viewport import Viewport
from viewport_pygame import Viewport
import pygame
import sys


class Application:
    WIDTH = 512
    HEIGHT = 512

    def __init__(self):
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mandelbrot")

        self.colormap = matplotlib.cm.get_cmap("twilight").colors
        self.palette = self.denormalize(self.colormap)

        self.center = -0.7435
        self.width = 3.5
        self.amount = 1
        self.max_iterations = 20

        self.mandelbrot_set = MandelbrotSet(max_iterations=self.max_iterations, escape_radius=1000)
        self.viewport = Viewport(self.display, self.center, self.width)
        self.paint(mandelbrot_set=self.mandelbrot_set, viewport=self.viewport, palette=self.palette, smooth=True)

        self.clock = pygame.time.Clock()

        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running:
            self.handle_events()
            self.draw()
            self.update()

    def stop(self):
        self.is_running = False
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()
                if event.key == pygame.K_SPACE:
                    self.mandelbrot_set.max_iterations += 128
                    self.paint(mandelbrot_set=self.mandelbrot_set, viewport=self.viewport, palette=self.palette, smooth=True)

            if event.type == pygame.MOUSEWHEEL:

                self.width -= self.amount * event.y
                self.viewport.width = self.width
                self.viewport.center = self.center
                self.paint(mandelbrot_set=self.mandelbrot_set, viewport=self.viewport, palette=self.palette,
                           smooth=True)
                print(self.width)


    def draw(self):
        #self.display.fill((255, 255, 255))

        pygame.display.update()

    def denormalize(self, palette):
        return [tuple(int(channel * 255) for channel in color) for color in palette]

    @staticmethod
    def paint(mandelbrot_set, viewport, palette, smooth):
        for pixel in viewport:
            stability = mandelbrot_set.stability(complex(pixel), smooth)
            index = int(min(stability * len(palette), len(palette) - 1))
            pixel.color = palette[index % len(palette)]

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        new_x, new_y = (mouse_pos[0] - self.WIDTH) / self.WIDTH, (mouse_pos[1] - self.HEIGHT) / self.HEIGHT

        self.center = complex(new_x, -new_y)











# colormap = matplotlib.cm.get_cmap("twilight").colors
# #palette = denormalize(colormap)
#
# mandelbrot_set = MandelbrotSet(max_iterations=20, escape_radius=1000)
#
# image = Image.new(mode="RGB", size=(512, 512))
#
# viewport = Viewport(image, center=-0.7435, width=3.5)
# #paint(mandelbrot_set, viewport, palette, smooth=True)
# image.show()


if __name__ == '__main__':
    app = Application()
    app.run()
    #print(complex((300 - 500) / 500, (300 - 500) / 500))



