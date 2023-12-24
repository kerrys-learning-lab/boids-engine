import geometry
import simulation.behaviors.wall_avoidance
import simulation.boids.boid
import simulation.boid_manager
import simulation.world

class TestNorthWallAvoider:

    def test_update(self, small_world: simulation.world.World, default_boid_manager: simulation.boid_manager.BoidManager):
        b = simulation.boids.boid.Boid(position=geometry.Point(5, 5), velocity=geometry.Vector(1, 1))

        uut = simulation.behaviors.wall_avoidance.NorthWallAvoider(default_boid_manager)

        for i in range(10):
            v = uut(1, b, small_world)
            if b.position.y + default_boid_manager.collision_avoidance_range > small_world.height:
                assert v.x == 0
                assert v.y < 0
            else:
                assert v.x == 0
                assert v.y == 0

            b.velocity += v
            b.position += b.velocity


class TestSouthWallAvoider:

    def test_update(self, small_world: simulation.world.World, default_boid_manager: simulation.boid_manager.BoidManager):
        b = simulation.boids.boid.Boid(position=geometry.Point(5, 5), velocity=geometry.Vector(-1, -1))

        uut = simulation.behaviors.wall_avoidance.SouthWallAvoider(default_boid_manager)

        for i in range(10):
            v = uut(1, b, small_world)

            if b.position.y - default_boid_manager.collision_avoidance_range < 0:
                assert v.x == 0
                assert v.y > 0
            else:
                assert v.x == 0
                assert v.y == 0

            b.velocity += v
            b.position += b.velocity


class TestEastWallAvoider:

    def test_update(self, small_world: simulation.world.World, default_boid_manager: simulation.boid_manager.BoidManager):
        b = simulation.boids.boid.Boid(position=geometry.Point(5, 5), velocity=geometry.Vector(1, 1))

        uut = simulation.behaviors.wall_avoidance.EastWallAvoider(default_boid_manager)

        for i in range(10):
            v = uut(1, b, small_world)
            if b.position.x + default_boid_manager.collision_avoidance_range > small_world.width:
                assert v.x < 0
                assert v.y == 0
            else:
                assert v.x == 0
                assert v.y == 0

            b.velocity += v
            b.position += b.velocity


class TestWestWallAvoider:

    def test_update(self, small_world: simulation.world.World, default_boid_manager: simulation.boid_manager.BoidManager):
        b = simulation.boids.boid.Boid(position=geometry.Point(5, 5), velocity=geometry.Vector(-1, -1))

        uut = simulation.behaviors.wall_avoidance.WestWallAvoider(default_boid_manager)

        for i in range(10):
            v = uut(1, b, small_world)
            if b.position.x - default_boid_manager.collision_avoidance_range < 0:
                assert v.x > 0
                assert v.y == 0
            else:
                assert v.x == 0
                assert v.y == 0

            b.velocity += v
            b.position += b.velocity
