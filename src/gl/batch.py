import pyglet
import pyglet.shapes
import geometry
from gl import colors


class Batch:
    BACKGROUND = pyglet.graphics.OrderedGroup(0)
    MIDDLEGROUND = pyglet.graphics.OrderedGroup(1)
    FOREGROUND = pyglet.graphics.OrderedGroup(2)

    def __init__(self):
        self._batch = None
        self._dirty = False
        self._shapes = []

    def __enter__(self):
        self._batch = pyglet.graphics.Batch()
        return self

    def add(self, count, mode, group, *data):
        self._batch.add(count, mode, group if group else Batch.MIDDLEGROUND, *data)
        self._dirty = True

    def add_triangles(self, vertices, color=None, group=None):
        size = len(vertices)
        color = color if color else colors.WHITE
        glVertices = []
        glColors = []
        for v in vertices:
            glVertices.append(v.x)
            glVertices.append(v.y)
            glColors.extend(color)

        self.add(size, pyglet.gl.GL_TRIANGLES, group,
                 ('v2f', glVertices), ('c3B', glColors))

    def add_lines(self, points, color=None, close=False, group=None):
        size = (len(points) - 1 + (1 if close else 0)) * 2
        color = color if color else colors.WHITE
        glPoints = []
        glColors = []
        for i in range(len(points) - 1):
            glPoints.append(points[i].x)
            glPoints.append(points[i].y)
            glPoints.append(points[i + 1].x)
            glPoints.append(points[i + 1].y)
            glColors.extend(color * 2)

        if close:
            glPoints.append(points[-1].x)
            glPoints.append(points[-1].y)
            glPoints.append(points[0].x)
            glPoints.append(points[0].y)
            glColors.extend(color * 2)

        self.add(size, pyglet.gl.GL_LINES, group,
                 ('v2f', glPoints), ('c3B', glColors))

    def add_points(self, points, color=None, group=None):
        points = points if type(points) is list else [points]
        color = color if color else colors.WHITE
        size = len(points)
        glPoints = []
        glColors = []

        for p in points:
            glPoints.append(p.x)
            glPoints.append(p.y)
            glColors.extend(color)

        self.add(size, pyglet.gl.GL_POINTS, group,
                 ('v2f', glPoints), ('c3B', glColors))

    def add_circles(self, circles, color=None, group=None, opacity=None):
        circles = circles if type(circles[0]) is list else [circles]
        for center, radius in circles:
            c = pyglet.shapes.Circle(center.x,
                                     center.y,
                                     radius,
                                     color=color if color else colors.WHITE,
                                     batch=self._batch,
                                     group=group if group else Batch.MIDDLEGROUND)

            if opacity:
                c.opacity = opacity
            self._shapes.append(c)

    def add_sector(self, point: geometry.Point, radius, start, sweep, color=None, group=None, opacity=None):
        s = pyglet.shapes.Sector(point.x,
                                 point.y,
                                 radius,
                                 angle=sweep,
                                 start_angle=start,
                                 color=color if color else colors.WHITE,
                                 batch=self._batch,
                                 group=group if group else Batch.MIDDLEGROUND)
        if opacity:
            s.opacity = opacity
        self._shapes.append(s)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None and exc_value is None and traceback is None:
            if self._dirty:
                self._batch.draw()
