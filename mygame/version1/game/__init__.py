import pyglet
import shapely
import random
import time
from shapely.ops import cascaded_union
from objects import *
from pyglet.window import mouse
"""import pyglet.app
import pyglet.window
import pyglet.graphics"""

ROOM_WIDTH = 62
ROOM_HEIGHT = 82

NUM_ITERATIONS = 1000

def fitness(furniture):
  '''room is a polygon, furniture is a list of polygons'''

  # furniture intersecting
  '''intersectionality = 0
  for i, poly_1 in enumerate(furniture):
    for j, poly_2 in enumerate(furniture):
      if i >= j:
        continue
      intersectionality += poly_1.intersection(poly_2).area'''
      
  # new furniture intersecting -- linear time, I think
  separateness = shapely.ops.cascaded_union(furniture).area

  # furniture outside bounds of room
  outside_room = Rectangle(ROOM_WIDTH // 2, ROOM_HEIGHT // 2, ROOM_WIDTH, ROOM_HEIGHT, 0, True)
  amount_outside = 0
  side_amount = 0
  for poly in furniture:
    amount_outside += poly.difference(outside_room).area
    dx = poly.x - ROOM_WIDTH // 2
    dy = poly.y - ROOM_HEIGHT // 2
    side_amount += math.sqrt(dx * dx + dy * dy)

  #return -intersectionality - amount_outside * 10 + side_amount * 10
  return separateness * 100 - amount_outside * 100 + side_amount * 10



class RoomArranger(object):

  def __init__(self):
    self.furniture = [
        ImmovableRectangle(6, 12, 12, 24, 0, True),  # wardrobes
        ImmovableRectangle(56, 12, 12, 24, 0, True),
        MovableRectangle(0, 0, 32, 15, 0, True),     # beds
        MovableRectangle(0, 0, 32, 15, 0, True),
        MovableRectangle(0, 0, 20, 12, 0, True),     # desks
        MovableRectangle(0, 0, 20, 12, 0, True),
        #MovableRectangle(0, 0, 5, 10, 0, True),     # desk drawers
        #MovableRectangle(0, 0, 5, 10, 0, True)
        MovableRectangle(0, 0, 30, 30, 0, False),     # negative space
    ]

  def get_mutated_furniture(self):
    l = []

    '''here furniture is a list of things with attributes x, y, width, height, rotation'''
    for rectangle in self.furniture:
      l.append(rectangle.mutatedCopy())
        
    return l

  def show_arrangement(self):
    '''here furniture is a list of things with attributes x, y, width, height, rotation'''
    #pyglet.gl.glColor3f(.8,.8,.8)


    for rectangle in self.furniture:
      if not rectangle.isVisible():
        continue
      pyglet.gl.glColor3f(random.uniform(0, .9), random.uniform(0, .9), random.uniform(0, .9))
      # redundant with shapely.geometry.Polygon's vertices
      '''points = []
      x_axis = [math.cos(rectangle.rotation), math.sin(rectangle.rotation)]
      y_axis = [-math.sin(rectangle.rotation), math.cos(rectangle.rotation)]
      for i in range(4):
        sign1 = (i / 2) * 2 - 1
        sign2 = ((((i + 1) % 4)) / 2) * 2 - 1
        points.append((rectangle.x + sign1 * rectangle.width * x_axis[0] / 2 + sign2 * rectangle.height * y_axis[0] / 2, rectangle.y + sign1 * rectangle.width * x_axis[1] / 2 + sign2 * rectangle.height * y_axis[1] / 2 ))'''
      #poly = shapely.geometry.polygon(zip(points))
      pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
      [0, 1, 2, 0, 2, 3],
      ('v2i', [int(coord * 10) for tuple in list(rectangle.exterior.coords[:-1]) for coord in tuple])
    )
    
  def find_good_arrangement(self):
    x = 0
    cur_fit = fitness(self.furniture)
    for i in xrange(NUM_ITERATIONS):
      #if cur_fit > 100:
      #  break

      f = self.get_mutated_furniture()
      fit = fitness(f)

      #print fit
      if fit > cur_fit:
        self.furniture = f
        cur_fit = fit
        #self.show_arrangement()
        x += 1
        print i, fit
    return x

ra = RoomArranger()

window = pyglet.window.Window(ROOM_WIDTH * 10, ROOM_HEIGHT * 10)

def randomize_furniture(furniture):
  new_furniture = []
  for rectangle in furniture:
    if rectangle.isMovable():
      new_furniture.append(MovableRectangle(random.randint(0, ROOM_WIDTH), random.randint(0, ROOM_HEIGHT), rectangle.width, rectangle.height, random.uniform(0, 3.1415926), rectangle.visible))
    else:
      new_furniture.append(ImmovableRectangle(rectangle.x, rectangle.y, rectangle.width, rectangle.height, rectangle.rotation, rectangle.visible))
  return new_furniture

@window.event
def on_draw():
  pyglet.gl.glClearColor(240,240,240,255)
  window.clear()
  '''

  pyglet.gl.glColor3f(.8,.8,.8)

  pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
    [0, 1, 2, 0, 2, 3],
    ('v2i', (100, 100,
             150, 100,
             150, 150,
             100, 150))
  )'''
  ra.show_arrangement()
  #print fitness(ra.furniture)

@window.event
def on_mouse_press(x, y, button, modifiers):
  if button == mouse.LEFT:
    ra.furniture = randomize_furniture(ra.furniture)
    print ra.find_good_arrangement()
    #ra.furniture = ra.get_mutated_furniture()
    #print fitness(ra.furniture)
    #ra.show_arrangement()

if __name__ == '__main__':
  pyglet.app.run()
