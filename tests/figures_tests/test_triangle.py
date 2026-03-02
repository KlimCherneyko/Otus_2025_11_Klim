from src.triangle import Triangle
from src.rectangle import Rectangle
import math
import pytest

class TestTriangle:
  def test_valid_triangle(self):
    triangle = Triangle(3,4,5)
    assert triangle.perimeter == 12
    assert triangle.area == 6
  
  @pytest.mark.parametrize("a, b, c",[
    (1,2,5),
    (-1,2,5),
    (0,1,5),
  ])
  def test_invalid_triangle(self, a, b, c):
    with pytest.raises(ValueError):
      Triangle(a,b,c)

  def test_summa_area_triangle_rectangle(self):
    triangle = Triangle(3,4,5)
    rectangle = Rectangle(5,10)
    expected = triangle.area + rectangle.area
    result = triangle.add_area(rectangle)
    assert expected == pytest.approx(result)
