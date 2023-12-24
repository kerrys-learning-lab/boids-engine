import base
import geometry
import numpy as np

NOT IMPLEMENTED

class MatchVelocity(base.Behavior):

    def velocityMatching(self, num, indexs, boids):
        matcher = geometry.Vector(0, 0)
        for i in np.nditer(indexs):
            matcher += boids[i].velocity

        matcher /= num
        matcher -= self.velocity

        return matcher * self.velocity_matching_weight
