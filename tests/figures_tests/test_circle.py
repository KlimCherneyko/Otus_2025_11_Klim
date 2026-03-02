from src.circle import Circle
from src.square import Square
import pytest
import math

class TestsCircle:

  def test_valid_radius_circle(self):
    circle = Circle(6)
    assert circle.radius == 6
    assert circle.perimeter == pytest.approx(2 * math.pi * 6)
    assert circle.area == pytest.approx(math.pi * 36)

  def test_circle_negative_radius(self):
    with pytest.raises(ValueError, match="Radius cannot be negative"):
      Circle(-5)

  def test_circle_zero_radius(self):
    circle = Circle(0)
    assert circle.radius == 0
    assert circle.perimeter == 0
    assert circle.area == 0
  
  def test_circle_square(self):
    circle = Circle(5)
    square = Square(4)
    result = circle.add_area(square)
    expected = math.pi * 25 + 16
    assert result == pytest.approx(expected)
