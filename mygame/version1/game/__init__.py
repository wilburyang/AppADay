import pyglet
import shapely
import random
"""import pyglet.app
import pyglet.window
import pyglet.graphics"""

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


def fitness(room, furniture):
  '''room is a polygon, furniture is a list of polygons'''
  
  # furniture intersecting
  intersectionality = 0
  for i, poly_1 in enumerate(furniture):
    for j, poly_2 in enumerate(furniture):
      if i == j:
        continue
      intersectionality += poly_1.intersect(poly_2).area()

  # furniture outside bounds of room
  outside_room = 0
  for poly in enumerate(furniture):
    outside_room += poly.difference(outside_room).area()

  return -intersectionality - outside_room*10

def mutate(rectangle):
  rectangle.x += random.uniform(-10, 10)
  rectangle.y += random.uniform(-10, 10)
  rectangle.rotation += random.uniform(-0.1, 0.1)

def generate_random_arrangement(furniture):
  '''here furniture is a list of things with attributes x, y, width, height, rotation'''
  for rectangle in furniture:
    for i in range(10):
      mutate(rectangle)

def show_arrangement(furniture):
  '''here furniture is a list of things with attributes x, y, width, height, rotation'''
  pyglet.gl.glColor3f(.8,.8,.8)

  
  for rectangle in furniture:
    points = []
    x_axis = [math.cos(rectangle.angle), math.sin(rectangle.angle)]
    y_axis = [-math.sin(rectangle.angle), math.cos(rectangle.angle)]
    for i in range(4):
      sign1 = (i / 2) * 2 - 1
      sign2 = ((((i + 1) % 4)) / 2) * 2 - 1
      points.append((rectangle.x + sign1 * rectangle.width * x_axis[0] / 2 + sign2 * rectangle.height * y_axis[0] / 2, rectangle.y + sign1 * rectangle.width * x_axis[1] / 2 + sign2 * rectangle.height * y_axis[1] / 2 ))
    #poly = shapely.geometry.polygon(zip(points))
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
    [0, 1, 2, 0, 2, 3],
    ('v2i', (points[0][0], points[0][1],
             points[1][0], points[1][1],
             points[2][0], points[2][1],
             points[3][0], points[3][1],))
  )


pyglet.app.run()
