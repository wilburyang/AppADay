import pyglet
import shapely
import random
from objects import *
from pyglet.window import mouse
"""import pyglet.app
import pyglet.window
import pyglet.graphics"""



class RoomArranger(object):

  def __init__(self):
    self.furniture = [Rectangle(10, 30, 20, 30, 3.14), Rectangle(50, 30, 20, 30, -.1)]

  def fitness(self):
    '''room is a polygon, furniture is a list of polygons'''

    # furniture intersecting
    intersectionality = 0
    for i, poly_1 in enumerate(self.furniture):
      for j, poly_2 in enumerate(self.furniture):
        if i == j:
          continue
        intersectionality += poly_1.intersect(poly_2).area()

    # furniture outside bounds of room
    outside_room = 0
    for poly in enumerate(self.furniture):
      outside_room += poly.difference(outside_room).area()

    return -intersectionality - outside_room * 10

  def generate_random_arrangement(self):

    '''here furniture is a list of things with attributes x, y, width, height, rotation'''
    for rectangle in self.furniture:
      for j in range(3):
        rectangle.mutate()

  def show_arrangement(self):
    '''here furniture is a list of things with attributes x, y, width, height, rotation'''
    pyglet.gl.glColor3f(.8,.8,.8)


    for rectangle in self.furniture:
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


ra = RoomArranger()

window = pyglet.window.Window(800, 600)

@window.event
def on_draw():
  pyglet.gl.glClearColor(240,0,0,255)
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

@window.event
def on_mouse_press(x, y, button, modifiers):
  if button == mouse.LEFT:
    ra.generate_random_arrangement()
    ra.show_arrangement()

if __name__ == '__main__':
  pyglet.app.run()
