import typing
import boids
import gl
import geometry
import math


class GlBoid(boids.Boid):

    def __init__(self,
                 world: 'boids.World',
                 config: dict = boids.Boid.DEFAULT_CONFIG,
                 position: geometry.Point = None,
                 velocity: geometry.Vector = None):
        super().__init__(world, config, position, velocity)
        self.color = gl.WHITE
        self._origin_body: typing.List[geometry.Point] = None
        self._body: typing.List[geometry.Point] = None
        self._velocity_indicator: typing.List[geometry.Point] = None
        self._view_indicator: typing.List[geometry.Point] = None
        self._body_tip: geometry.Point = None
        self.body_theta = math.atan(0.5)

    def batch(self, glBatch: gl.Batch, **kwargs):
        glBatch.add_triangles(self.body, color=self.color)

        if kwargs.get('velocity_indicator'):
            glBatch.add_lines(self.velocity_indicator, color=gl.colors.ORANGE)

        if kwargs.get('view_indicator'):
            glBatch.add_sector(self.view_indicator[0],
                               self.view_indicator[1],
                               self.view_indicator[2],
                               self.view_indicator[3],
                               opacity=25,
                               color=gl.colors.YELLOW,
                               group=gl.Batch.BACKGROUND)

        if kwargs.get('collision_indicator'):
            glBatch.add_circles(self.collision_indicator,
                                color=gl.colors.DARK_RED,
                                group=gl.Batch.BACKGROUND,
                                opacity=75)

    @property
    def body(self):
        if self._body is None:
            self._body = [vertex + self.position.vector for vertex in self.origin_body]
            self._body = [vertex.rotateXY(self.velocity.angleXY, self.position) for vertex in self._body]

        return self._body

    @property
    def origin_body(self):
        #  y |
        #    |
        # p1 |
        # | \
        # |   >-p2---------
        # | /             x
        # p3
        if self._origin_body is None:
            self._origin_body = (geometry.Point(-self.size / 2, -self.size / 2),
                                 geometry.Point(self.size / 2, 0),  # At BODY_TIP_INDEX
                                 geometry.Point(-self.size / 2, self.size / 2))

        return self._origin_body

    @property
    def velocity_indicator(self):
        if self._velocity_indicator is None:
            self._velocity_indicator = (self.body_tip, self.body_tip + self.velocity)

        return self._velocity_indicator

    @property
    def view_indicator(self):
        if self._view_indicator is None:
            self._view_indicator = (self.position,
                                    self.view_range,
                                    -(self.view_angle/2) + self.velocity.angleXY,
                                    self.view_angle)

        return self._view_indicator

    @property
    def collision_indicator(self):
        return (self.position, self.collision_avoidance_range)

    @property
    def body_tip(self):
        if self._body_tip is None:
            self._body_tip = self.position + geometry.Vector(self.size/2 * math.cos(self.velocity.angleXY),
                                                             self.size/2 * math.sin(self.velocity.angleXY))
        return self._body_tip

    @ property
    def color(self):
        return self._color

    @ color.setter
    def color(self, value):
        self._color = value

    def _set_dirty(self):
        self._body = None
        self._origin_body = None
        self._velocity_indicator = None
        self._body_tip = None
        self._view_indicator = None
        return super()._set_dirty()
