
import geometry
import math
import simulation.behaviors.base
import simulation.boids.boid
import simulation.boids.traits
import simulation.world

class NormalizeVelocity(simulation.behaviors.base.Behavior):

    def __init__(self, boid_traits: simulation.boids.traits.Traits):
        super().__init__(simulation.behaviors.base.LATE_ORDER, [simulation.behaviors.base.SPEED])
        self._boid_traits = boid_traits

    def __call__(self, dt, boid: simulation.boids.boid.Boid, world: simulation.world.World):
        nominal_speed = max(self._boid_traits.max_speed * 0.75, self._boid_traits.min_speed)
        delta_v = geometry.Vector(0, 0)

        if boid.velocity.magnitude > (nominal_speed + simulation.behaviors.base.DELTA_V_INCR):
            delta_v.x = -1 * simulation.behaviors.base.DELTA_V_INCR * math.cos(boid.velocity.angleXY) * self._boid_traits.velocity_normalization_weight
            delta_v.y = -1 * simulation.behaviors.base.DELTA_V_INCR * math.sin(boid.velocity.angleXY) * self._boid_traits.velocity_normalization_weight
        if boid.velocity.magnitude < (nominal_speed - simulation.behaviors.base.DELTA_V_INCR):
            delta_v.x = simulation.behaviors.base.DELTA_V_INCR * math.cos(boid.velocity.angleXY) * self._boid_traits.velocity_normalization_weight
            delta_v.y = simulation.behaviors.base.DELTA_V_INCR * math.sin(boid.velocity.angleXY) * self._boid_traits.velocity_normalization_weight

        if delta_v.magnitude > 0:
            self.logger.debug('Velocity normalization in progress: p={p}, v={v}, dv={dv}'.format(p=str(boid.position),
                                                                                                 v=str(boid.velocity),
                                                                                                 dv=str(delta_v)))

        return delta_v
