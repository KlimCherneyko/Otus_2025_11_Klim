from src.figure import Figure

class Square(Figure):
    def __init__(self, side):
        if side <= 0:
            raise ValueError("Square side must be greater than 0")
        self.side = side
    @property
    def area(self):
        return self.side * self.side
    @property
    def perimeter(self):
        return self.side *4
