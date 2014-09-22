import shapely
import math
import random
from shapely.geometry import Polygon


def rotate(t, rotation):
  return (t[0] * math.cos(rotation) - t[1] * math.sin(rotation), t[0] * math.sin(rotation) + t[1] * math.cos(rotation))

mx = [1, -1, -1, 1]
my = [1, 1, -1, -1]

class Rectangle(Polygon):

  def __init__(self, x, y, width, height, rotation):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.rotation = rotation

    w2 = width / 2.
    h2 = height / 2.
    l = []
    for k in range(4):
      l.append(rotate((mx[k] * w2, my[k] * h2), rotation))

    l = [(a[0] + x, a[1] + y) for a in l]
    Polygon.__init__(self, l)

  def mutate(self):
    self.x += random.uniform(-10, 10)
    self.y += random.uniform(-10, 10)
    self.rotation += random.uniform(-0.1, 0.1)
    self.__init__(self.x, self.y, self.width, self.height, self.rotation)

  def mutatedCopy(self):
    if self.isMovable():
      return MovableRectangle(self.x + random.uniform(-10, 10), self.y + random.uniform(-10, 10), self.width, self.height, self.rotation + random.uniform(-0.1, 0.1))
    else:
      return MovableRectangle(self.x + random.uniform(-10, 10), self.y + random.uniform(-10, 10), self.width, self.height, self.rotation + random.uniform(-0.1, 0.1))

  def isMovable(self):
    # to be implemented in subclasses
    raise NotImplementedError

class MovableRectangle(Rectangle):
  def __init__(self, x, y, width, height, rotation):
    Rectangle.__init__(self, x, y, width, height, rotation)

  def isMovable(self):
    return True

class ImmovableRectangle(Rectangle):
  def __init__(self, x, y, width, height, rotation):
    Rectangle.__init__(self, x, y, width, height, rotation)

  def isMovable(self):
    return False


