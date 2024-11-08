import numpy as np
import matplotlib.pyplot as plt

class Checker:
    def __init__(self, resolution, tile_size):
        self.resolution = resolution
        self.tile_size = tile_size
        self.output = np.zeros((resolution, resolution), dtype=int)

    def draw(self):
        # Generate the checkerboard pattern
        for i in range(0, self.resolution, self.tile_size * 2):
            for j in range(0, self.resolution, self.tile_size * 2):
                # Set white tiles
                self.output[i:i + self.tile_size, j + self.tile_size:j + 2 * self.tile_size] = 1
                self.output[i + self.tile_size:i + 2 * self.tile_size, j:j + self.tile_size] = 1
        return self.output.copy()  # Ensure to return a copy


    def show(self):
        plt.imshow(self.output, cmap='gray', vmin=0, vmax=1)
        plt.title('Checkerboard Pattern')
        plt.colorbar()
        plt.show()

class Circle:
    def __init__(self, resolution, radius, center):
        self.resolution = resolution
        self.radius = radius
        self.center = center
        self.output = np.zeros((resolution, resolution), dtype=int)

    def draw(self):
        # Create the binary circle pattern
        y, x = np.ogrid[:self.resolution, :self.resolution]
        mask = (x - self.center[0])**2 + (y - self.center[1])**2 <= self.radius**2
        self.output[mask] = 1
        return self.output.copy()  # Ensure to return a copy

    def show(self):
        plt.imshow(self.output, cmap='gray', vmin=0, vmax=1)
        plt.title('Circle Pattern')
        plt.colorbar()
        plt.show()


class Spectrum:
    def __init__(self, size):
        self.size = size
        self.output = np.zeros((size, size, 3), dtype=float)

    def draw(self):
        # Creating a gradient for each color channel
        x = np.linspace(0, 1, self.size)
        y = np.linspace(0, 1, self.size)
        X, Y = np.meshgrid(x, y)
        # Assign gradients across different dimensions
        self.output[:, :, 0] = X  # Red gradient across x
        self.output[:, :, 1] = Y  # Green gradient across y
        self.output[:, :, 2] = 1 - X  # Blue gradient from 1 to 0 across x
        return self.output.copy()  # Ensure to return a copy

    def show(self):
        plt.imshow(self.output)
        plt.title('RGB Color Spectrum')
        plt.show()




# # # Instances to display patterns
# checker = Checker(400, 40)
# checker.draw()
# checker.show()

# circle = Circle(400, 100, (200, 200))
# circle.draw()
# circle.show()

# spectrum = Spectrum(400)
# spectrum.draw()
# spectrum.show()