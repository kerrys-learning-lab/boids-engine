import math
from geometry import point
import geometry


class Vector(object):

    @staticmethod
    def fromPoints(start: 'point.Point', end: 'point.Point'):
        return Vector(end.x - start.x, end.y - start.y, end.z - start.z)

    @staticmethod
    def fromConfig(config: dict):
        return Vector(config['x'], config['y'], config.get('z', 0))

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

    def __eq__(self, other: 'Vector'):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __iadd__(self, other: 'Vector') -> 'Vector':
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other: 'Vector') -> 'Vector':
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, value) -> 'Vector':
        return Vector(self.x * value, self.y * value, self.z * value)

    def __imul__(self, value) -> 'Vector':
        self.x *= value
        self.y *= value
        self.z *= value
        return self

    def __itruediv__(self, value) -> 'Vector':
        self.x /= value
        self.y /= value
        self.z /= value
        return self

    def __truediv__(self, value) -> 'Vector':
        result = self.clone()
        result /= value
        return result

    def __str__(self):
        return '[{x:.4f}, {y:.4f}, {z:.4f}] (mag: {m:.2f}, angle: {a:.2f})'.format(x=self.x, y=self.y, z=self.z, m=self.magnitude, a=math.degrees(self.angleXY))

    def clone(self) -> 'Vector':
        return Vector(self.x, self.y, self.z)

    def rotateXY(self, theta, pivot: 'point.Point' = None) -> 'Vector':
        pivot = pivot if pivot else geometry.Point(0, 0)

        return Vector((self.x - pivot.x) * math.cos(theta) - (self.y - pivot.y) * math.sin(theta) + pivot.x,
                      (self.x - pivot.x) * math.sin(theta) + (self.y - pivot.y) * math.cos(theta) + pivot.y)

    def dot(self, other: 'Vector'):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def angleToXY(self, other: 'Vector'):
        ''' Returns the angle in radians tended from self to other '''
        return other.angleXY - self.angleXY

    @property
    def unit(self) -> 'Vector':
        if self._unit is None:
            self._unit = self / self.magnitude
        return self._unit

    @property
    def magnitude(self):
        if self._magnitude is None:
            self._magnitude = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        return self._magnitude

    @property
    def angleXY(self):
        if self._angle is None:
            self._angle = math.atan2(self.y, self.x)
        return self._angle

    def _set_dirty(self):
        self._magnitude = None
        self._angle = None
        self._unit = None

    def to_json(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}