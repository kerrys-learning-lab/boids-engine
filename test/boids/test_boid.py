import geometry
import pytest
import simulation.boids.boid
import simulation.boid_manager
import simulation.world

class TestBoid:

    def test_update(self, small_world: simulation.world.World, default_boid_manager: simulation.boid_manager.BoidManager):
        b = simulation.boids.boid.Boid(position=geometry.Point(0, 0), velocity=geometry.Vector(1, 1))
        default_boid_manager.avoid_walls = False
        default_boid_manager.normalize_velocity = False
        for i in range(1, 10):
            b.update(1)
            assert b.position == geometry.Point(i, i)
