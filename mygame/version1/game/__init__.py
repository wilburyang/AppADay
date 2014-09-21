import pyglet
"""import pyglet.app
import pyglet.window
import pyglet.graphics"""

window = pyglet.window.Window(800, 600)


@window.event
def on_draw():
  pyglet.gl.glClearColor(240,0,0,255)
  window.clear()
  
  
  pyglet.gl.glColor3f(.8,.8,.8)

  pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
    [0, 1, 2, 0, 2, 3],
    ('v2i', (100, 100,
             150, 100,
             150, 150,
             100, 150))
  )


pyglet.app.run()
