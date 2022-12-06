# import resource
import threading
from PIL import Image
import matplotlib.cm
import numpy as np
from mandelbrot import MandelbrotSet
#from viewport import Viewport
from viewport_pygame import Viewport
from numba import jit, cuda
import pygame
import sys


class Application:
    WIDTH = 700
    HEIGHT = 700
    FPS = 0

    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font("D:/fonts/Roboto-Black.ttf", 20)
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mandelbrot")
        self.clock = pygame.time.Clock()


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
        self.smooth = True

        self.mandelbrot_set = MandelbrotSet(max_iterations=self.max_iterations, escape_radius=1000)
        self.viewport = Viewport(self.display, self.center, self.width)
        self.paint(mandelbrot_set=self.mandelbrot_set, viewport=self.viewport, palette=self.palette, smooth=self.smooth)


        self.is_running = False
        self.is_debug = False

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

                    self.paint(mandelbrot_set=self.mandelbrot_set, viewport=self.viewport, palette=self.palette, smooth=self.smooth)

            if event.type == pygame.MOUSEWHEEL:
                pygame.display.set_caption(f"Zoom...")
                self.zoom_ratio += 0.2 * event.y
                self.viewport.width = 10 ** self.zoom_ratio
                self.viewport.center = self.center

                self.paint(mandelbrot_set=self.mandelbrot_set, viewport=self.viewport, palette=self.palette,
                           smooth=self.smooth)
                #print(self.viewport.width)

    def draw(self):
        pygame.display.flip()

    def denormalize(self, palette):
        return [tuple(int(channel * 255) for channel in color) for color in palette]


    def paint(self, mandelbrot_set, viewport, palette, smooth):
        #n = 0
        #self.painting_progress = 0
        time_start = pygame.time.get_ticks() / 1000
        self.display.fill((255, 255, 255))
        for pixel in viewport:
            #n += 1

            stability = mandelbrot_set.stability(complex(pixel), smooth)
            index = int(min(stability * len(palette), len(palette) - 1))

            if pixel.color[:3] != palette[index % len(palette)]:
                pixel.color = palette[index % len(palette)]

            #self.painting_progress = (n / (self.WIDTH * self.HEIGHT)) * 100
            #print(f"{int(self.painting_progress)}%")



        pygame.display.set_caption("Done!")
        time_end = pygame.time.get_ticks() / 1000
        print(time_end - time_start)


    def update(self):
        pos_x, pos_y = pygame.mouse.get_pos()

        self.center = complex(pos_x, -pos_y) * self.viewport.scale + self.viewport.offset
        self.debug()

        #self.viewport.center = self.center
        #print(self.viewport.center)

    def debug(self):
        if self.is_debug:
            self.display.fill((255, 255, 255))
            self.text_surf = self.font.render(str(self.center), True, (0, 0, 0))
            self.display.blit(self.text_surf, pygame.mouse.get_pos())



if __name__ == '__main__':
    app = Application()
    app.run()



