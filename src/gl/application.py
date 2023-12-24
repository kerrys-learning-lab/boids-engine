import gl
import pyglet

# fps_display = pyglet.window.FPSDisplay(window=window)


class Application:

    def __init__(self, bounds, caption=''):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        self.window = pyglet.window.Window(int(bounds.x), int(bounds.y),
                                           fullscreen=False,
                                           caption=caption)

        self.window.push_handlers(on_draw=self.on_draw)

    def schedule(self, f):
        pyglet.clock.schedule(f)

    def run(self):
        pyglet.app.run()

    def redraw(self):
        pass

    def create_batch(self):
        return gl.Batch()

    def on_draw(self):
        pyglet.gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        self.window.clear()
        pyglet.gl.glLoadIdentity()

        self.redraw()
        # fps_display.draw()
