from abc import ABC, abstractmethod


class Figure(ABC):

    @property
    @abstractmethod
    def area(self):
        pass

    @property
    @abstractmethod
    def perimeter(self):
        pass

    def add_area(self, figure):
        if not isinstance(figure, Figure):
            raise ValueError("Argument must be a Figure instance")
        return self.area + figure.area
