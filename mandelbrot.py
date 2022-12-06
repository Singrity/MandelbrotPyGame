from dataclasses import dataclass
from math import log
import numpy as np

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def escape_count(self, c: complex, smooth=False) -> float or int:
        #
        z = 0
        for iteration in range(self.max_iterations):
            #
        #
            z = z ** 2 + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iteration + 1 - log(log(abs(z))) / log(2)
                else:
                    return iteration
        return self.max_iterations

    def escape_count_optimized(self, c:complex, smooth=False):
        z = np.array([0], dtype="complex")
        for iteration in range(self.max_iterations):
            z = np.append(z, z[z.size - 1] ** 2 + c)
        if abs(z.all()) > self.escape_radius:
            if smooth:
                return np.argwhere(abs(z) > self.escape_radius) - np.log(np.log(abs(z))) / np.log(2)
            else:
                return np.argwhere(abs(z) > self.escape_radius) - 1
        return self.max_iterations
        #print(z)

    def stability_optimized(self, c: complex, smooth=False, clamp=True):
        value = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1


set = MandelbrotSet(20, 1000)
set.stability_optimized(1, True)
