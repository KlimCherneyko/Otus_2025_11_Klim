from src.square import Square
from src.triangle import Triangle
import math
import pytest

class TestSquare:

  def test_valid_square(self):
    square = Square(10)
    assert square.perimeter == 40
    assert square.area == 100

  @pytest.mark.parametrize("a", [
    (-10),
    (0)
    ])
  def test_invalid_square(self, a):
    with pytest.raises(ValueError):
      Square(a)

  def test_summa_area_square_triangel(self):
    square = Square(10)
    triangle = Triangle(3, 5, 4)
    expected = square.area + triangle.area
    result = square.add_area(triangle)
    assert result == pytest.approx(expected)