import resource
import threading
from PIL import Image
import matplotlib.cm
import numpy as np
from mandelbrot import MandelbrotSet
#from viewport import Viewport
from viewport_pygame import Viewport
import pygame
import sys


class Application:
    WIDTH = 300
    HEIGHT = 300

    def __init__(self):
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mandelbrot")

        self.painting_progress = 0

        self.colormap = matplotlib.cm.get_cmap("twilight").colors
        self.palette = self.denormalize(self.colormap)

        self.iter_ratio = 5
        self.zoom_ratio = 0
        #self.center = -0.743643887037158704752191506114774 + 0.131825904205311970493132056385139j
        self.center = complex(0, 0)
        self.width = 4 * 10 ** self.zoom_ratio
        self.amount = 1
        self.max_iterations = 2 ** self.iter_ratio

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
        print(self.viewport.center, self.viewport.width)
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
                    pygame.display.set_caption(f"Increasing max_iterations...")
                    self.iter_ratio += 1
                    self.mandelbrot_set.max_iterations = 2 ** self.iter_ratio

                    self.paint(mandelbrot_set=self.mandelbrot_set, viewport=self.viewport, palette=self.palette, smooth=True)

            if event.type == pygame.MOUSEWHEEL:
                pygame.display.set_caption(f"Zoom...")
                self.zoom_ratio += 0.3 * event.y
                self.viewport.width = 10 ** self.zoom_ratio
                self.viewport.center = self.center

                self.paint(mandelbrot_set=self.mandelbrot_set, viewport=self.viewport, palette=self.palette,
                           smooth=True)
                print(self.viewport.width)

    def draw(self):
        pygame.display.flip()

    def denormalize(self, palette):
        return [tuple(int(channel * 255) for channel in color) for color in palette]

    #@staticmethod
    def paint(self, mandelbrot_set, viewport, palette, smooth):
        n = 0
        self.painting_progress = 0
        for pixel in viewport:
            n += 1

            stability = mandelbrot_set.stability(complex(pixel), smooth)
            index = int(min(stability * len(palette), len(palette) - 1))

            self.painting_progress = (n / (self.WIDTH * self.HEIGHT)) * 100
            print(f"{int(self.painting_progress)}%")

            if pixel.color[:3] != palette[index % len(palette)]:
                pixel.color = palette[index % len(palette)]

        pygame.display.set_caption("Done!")

    def update(self):
        pos_x, pos_y = pygame.mouse.get_pos()

        self.center = complex(pos_x, -pos_y) * self.viewport.scale + self.viewport.offset
        #self.viewport.center = self.center
        #print(self.viewport.center)


if __name__ == '__main__':
    app = Application()
    app.run()



