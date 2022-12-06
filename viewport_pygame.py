from dataclasses import dataclass


class Viewport:

    def __init__(self, surface, center: complex, width: float):
        self.image = surface
        self.center = center
        self.width = width

    @property
    def height(self):
        return self.scale * self.image.get_height()

    @property
    def offset(self):
        return self.center + complex(-self.width, self.height) / 2

    @property
    def scale(self):
        return self.width / self.image.get_width()

    def __iter__(self):
        #pygame.display.flip()
        for y in range(0, self.image.get_height()):
            for x in range(self.image.get_width()):
                yield Pixel(self, x, y)


@dataclass
class Pixel:
    viewport: Viewport
    x: int
    y: int

    @property
    def color(self):
        return self.viewport.image.get_at((self.x, self.y))

    @color.setter
    def color(self, value):
        self.viewport.image.set_at((self.x, self.y), value)

    def __complex__(self):
        return complex(self.x, -self.y) * self.viewport.scale + self.viewport.offset
