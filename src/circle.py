from figure import Figure
import math
class Circle(Figure):
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self.radius = radius

    @property
    def area(self):
       return math.pi * self.radius ** 2

    @property
    def perimeter(self):
        return 2* math.pi * self.radius

v = Circle(25)
print(v.area)
print(v.perimeter)