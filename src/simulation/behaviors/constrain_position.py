import geometry
import simulation.behaviors.base
import simulation.boids.boid
import simulation.boids.traits
import simulation.world

class ConstrainPosition(simulation.behaviors.base.Behavior):

    def __init__(self, boid_traits: simulation.boids.traits.Traits):
        super().__init__(simulation.behaviors.base.LATE_ORDER, [simulation.behaviors.base.SPEED])
        self._boid_traits = boid_traits

    def __call__(self, dt, boid: simulation.boids.boid.Boid, world: simulation.world.World, p: geometry.Point):
        p = p.clone()

        if not self._boid_traits.avoid_walls:
            if boid.position.x >= world.width:
                p.x = 0
            elif boid.position.x < 0:
                p.x = world.width
            if boid.position.y >= world.height:
                p.y = 0
            elif boid.position.y < 0:
                p.y = world.height

        return p
