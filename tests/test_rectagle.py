from src.rectangle import Rectangle
from src.circle import Circle
import math
import pytest

class TestRectagle:

  def test_valid_rectagle(self):
    rect = Rectangle(5, 10)
    assert rect.width == 5
    assert rect.height == 10
    assert rect.area == 50
    assert rect.perimeter == 30

  @pytest.mark.parametrize("width, height", [
    (-5, 10),
    (5, -10),
    (-5, -10),
    (0, 10),
    (5, 0),
    (0, 0),
])
  def test_rectangle_invalid_dimensions(self, width, height):
    with pytest.raises(ValueError):
        Rectangle(width, height)
  
  def test_summa_area_reactgle_circle(self):
    reactgel = Rectangle(5, 10)
    circle = Circle(5)
    result = circle.add_area(reactgel)
    expected = math.pi * 25 + 50
    assert result == pytest.approx(expected)
