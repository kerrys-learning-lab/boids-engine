import geometry
import simulation.behaviors.base
import simulation.boids.boid
import simulation.boids.traits
import simulation.world

class WallAvoider(simulation.behaviors.base.Behavior):

    def __init__(self, boid_traits: simulation.boids.traits.Traits, delta_v: geometry.Vector):
        super().__init__(simulation.behaviors.base.MED_ORDER,
                         [simulation.behaviors.base.COLLISION_AVOIDANCE_TAG, simulation.behaviors.base.WALL_AVOIDANCE_TAG, self.__class__.__name__])
        self._boid_traits = boid_traits
        self.delta_v = delta_v

    def _dist(self, boid: simulation.boids.boid.Boid, world: simulation.world.World):
        return None

    def __call__(self, dt, boid: simulation.boids.boid.Boid, world: simulation.world.World):
        dist = self._dist(boid, world)
        delta_v = geometry.Vector(0, 0)

        if dist < self._boid_traits.collision_avoidance_range:
            accelerant = ((self._boid_traits.collision_avoidance_range * self._boid_traits.collision_avoidance_weight) / max(dist, 0.1))**2
            delta_v += self.delta_v * accelerant

            self.logger.debug('Wall avoidance in progress: p={p}, v={v}, dv={dv}, d={d:.04f}'.format(p=str(boid.position),
                                                                                                     v=str(
                                                                                                         boid.velocity),
                                                                                                     dv=str(delta_v),
                                                                                                     d=dist))

        return delta_v


class NorthWallAvoider(WallAvoider):

    def __init__(self, boid_traits: simulation.boids.traits.Traits):
        super().__init__(boid_traits, geometry.Vector(0, -simulation.behaviors.base.DELTA_V_INCR))

    def _dist(self, boid: simulation.boids.boid.Boid, world: simulation.world.World):
        return world.height - boid.position.y


class SouthWallAvoider(WallAvoider):

    def __init__(self, boid_traits: simulation.boids.traits.Traits):
        super().__init__(boid_traits, geometry.Vector(0, simulation.behaviors.base.DELTA_V_INCR))

    def _dist(self, boid: simulation.boids.boid.Boid, world: simulation.world.World):
        # obviously, assumes wold's southern boundary is 0
        return boid.position.y


class EastWallAvoider(WallAvoider):

    def __init__(self, boid_traits: simulation.boids.traits.Traits):
        super().__init__(boid_traits, geometry.Vector(-simulation.behaviors.base.DELTA_V_INCR, 0))

    def _dist(self, boid: simulation.boids.boid.Boid, world: simulation.world.World):
        return world.width - boid.position.x


class WestWallAvoider(WallAvoider):

    def __init__(self, boid_traits: simulation.boids.traits.Traits):
        super().__init__(boid_traits, geometry.Vector(simulation.behaviors.base.DELTA_V_INCR, 0))

    def _dist(self, boid: simulation.boids.boid.Boid, world: simulation.world.World):
        # obviously, assumes wold's western boundary is 0
        return boid.position.x
