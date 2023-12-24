import geometry
import simulation.behaviors.base
import simulation.boids.boid
import simulation.boids.traits
import simulation.world

class ConstrainVelocity(simulation.behaviors.base.Behavior):

    def __init__(self, boid_traits: simulation.boids.traits.Traits):
        super().__init__(simulation.behaviors.base.LATE_ORDER, [simulation.behaviors.base.SPEED])
        self._boid_traits = boid_traits

    def __call__(self, dt, boid: simulation.boids.boid.Boid, world: simulation.world.World, v: geometry.Vector):
        # Constrain Velocity between min/max
        speed = boid.velocity.magnitude + 1
        speed_scalar = 1
        speed_scalar = (self._boid_traits.max_speed / speed) if speed > self._boid_traits.max_speed else speed_scalar
        speed_scalar = (self._boid_traits.min_speed / speed) if speed < self._boid_traits.min_speed else speed_scalar

        v = v.clone()

        if speed_scalar != 1:
            self.logger.debug('Velocity before scaling: {v}'.format(v=boid.velocity))

            v *= speed_scalar

            self.logger.debug('Velocity after scaling:  {v} (scalar: {s})'.format(v=boid.velocity,
                                                                                  s=speed_scalar))

        return v
