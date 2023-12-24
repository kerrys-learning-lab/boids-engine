from geometry import vector
import math

class Point(object):

    @staticmethod
    def fromConfig(config: dict):
        return Point(config['x'], config['y'], config.get('z', 0))

    def __init__(self, x, y, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self._set_dirty()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._set_dirty()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._set_dirty()

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value
        self._set_dirty()

    def __iadd__(self, v: 'vector.Vector') -> 'Point':
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def __add__(self, v: 'vector.Vector'):
        result = self.clone()
        result += v
        return result

    def __str__(self):
        return '({x:.4f}, {y:.4f}, {z:.4f})'.format(x=self.x, y=self.y, z=self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def rotateXY(self, theta, pivot: 'Point' = None):
        pivot = pivot if pivot else Point(0, 0)

        return Point((self.x - pivot.x) * math.cos(theta) - (self.y - pivot.y) * math.sin(theta) + pivot.x,
                     (self.x - pivot.x) * math.sin(theta) + (self.y - pivot.y) * math.cos(theta) + pivot.y)

    def clone(self) -> 'Point':
        return Point(self.x, self.y, self.z)

    @property
    def vector(self):
        if self._vector is None:
            self._vector = vector.Vector(self.x, self.y, self.z)
        return self._vector

    def _set_dirty(self):
        self._vector = None

    def to_json(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}