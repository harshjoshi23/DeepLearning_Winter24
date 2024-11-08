from pattern import Checker, Circle, Spectrum

def main():
    # Create and display a Checkerboard
    checker = Checker(800, 100)
    checker.draw()
    checker.show()

    # Create and display a Circle
    circle = Circle(800, 200, (400, 400))
    circle.draw()
    circle.show()

    spectrum = Spectrum(400)
    spectrum.draw()
    spectrum.show()

if __name__ == "__main__":
    main()
