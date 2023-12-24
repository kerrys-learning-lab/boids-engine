import base
import boids
import geometry
import numpy as np


NOT IMPLEMENTED

class AvoidCollision(base.Behavior):

    def __init__(self, boid_manager: boids.BoidManager):
        super().__init__(base.LATE_ORDER, [base.SPEED])
        self._boid_manager = boid_manager

    def __call__(self, dt, boid: boids.Boid, world: boids.World, p: geometry.Point):
        # def collisionAvoidence(self, indexs, boids):
        avoider = geometry.Vector(0, 0)
        for i in range(len(self._boid_manager)):
            other = boids[i]
            v = geometry.Vector.fromPoints(boid.position, boids[i].position)

            # if self.id == 0:
            #     self.logger.debug('{id}.collisionAvoidance({other}): {v}'.format(id=self.id, other=other.id, v=v))

            if v.magnitude < self.collision_avoidance_range and abs(v.angleXY) < (self.view_angle/2):
                if self.id == 0:
                    self.logger.debug('{id}.collisionAvoidance({other}): COLLISION DANGER'.format(
                        id=self.id, other=other.id))
                    self.logger.debug(v)
                avoider -= v

        return avoider * self.collision_avoidance_weight
