import geometry
import simulation.boids.boid
import simulation.boid_manager
import simulation.world

class TestNeighbors:

    def test_1st_quad_1st_quad_visible(self, default_boid_manager: simulation.boid_manager.BoidManager):
        b1 = simulation.boids.boid.Boid(position=geometry.Point(5, 5), velocity=geometry.Vector(1, 1))
        b2 = simulation.boids.boid.Boid(position=geometry.Point(10, 10), velocity=geometry.Vector(1, 1))

        n = simulation.boid_manager.Neighbors(b1, b2, default_boid_manager.view_angle_radians, default_boid_manager.view_range)

        assert n.is_neighbor_visible()

    def test_1st_quad_1st_quad_not_visible(self, default_boid_manager: simulation.boid_manager.BoidManager):
        b1 = simulation.boids.boid.Boid(position=geometry.Point(5, 5), velocity=geometry.Vector(-5, -5))
        b2 = simulation.boids.boid.Boid(position=geometry.Point(10, 10), velocity=geometry.Vector(1, 1))

        n = simulation.boid_manager.Neighbors(b1, b2, default_boid_manager.view_angle_radians, default_boid_manager.view_range)

        assert not n.is_neighbor_visible()

    def test_1st_quad_2nd_quad_visible(self, default_boid_manager: simulation.boid_manager.BoidManager):
        b1 = simulation.boids.boid.Boid(position=geometry.Point(5, 5), velocity=geometry.Vector(-5, -5))
        b2 = simulation.boids.boid.Boid(position=geometry.Point(10, -20), velocity=geometry.Vector(1, 1))

        n = simulation.boid_manager.Neighbors(b1, b2, default_boid_manager.view_angle_radians, default_boid_manager.view_range)

        assert n.is_neighbor_visible()

    def test_1st_quad_2nd_quad_not_visible(self, default_boid_manager: simulation.boid_manager.BoidManager):
        b1 = simulation.boids.boid.Boid(position=geometry.Point(5, 5), velocity=geometry.Vector(-5, -5))
        b2 = simulation.boids.boid.Boid(position=geometry.Point(10, -30), velocity=geometry.Vector(1, 1))

        n = simulation.boid_manager.Neighbors(b1, b2, default_boid_manager.view_angle_radians, default_boid_manager.view_range)

        assert n.is_neighbor_visible()
