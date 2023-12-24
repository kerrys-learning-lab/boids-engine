import base
import geometry
import numpy as np

NOT IMPLEMENTED

class SteerTowardsFlockCenter(base.Behavior):

    def flockCentering(self, num, indexs, boids):
        xTotal, yTotal = 0, 0
        for i in np.nditer(indexs):
            xTotal += boids[i].position.x
            yTotal += boids[i].position.y

            self.boid_mask[i] = 0

        return geometry.Vector(xTotal/num - self.position.x, yTotal/num - self.position.y) * self.flock_centering_weight
