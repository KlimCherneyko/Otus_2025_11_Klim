from figure import Figure
class Rectangle(Figure):
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("Rectangle width and height must be positive")
        self.width = width
        self.height = height
    @property
    def area(self):
        return self.width * self.height
    @property
    def perimeter(self):
        return 2 * (self.width + self.height)

s = Rectangle(width=6, height=10)

print(s.area)
print(s.perimeter)