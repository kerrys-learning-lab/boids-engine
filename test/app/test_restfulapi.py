import pytest
import app
import boidsapi.boids
import simulation
import simulation.boid_manager
import simulation.world
import werkzeug.exceptions

class TestRestfulApi:

    def test_api_v1_get_simulation(self,
                                   default_simulation: simulation.SimulationManager,
                                   small_world: simulation.world.World,
                                   default_boid_manager: simulation.boid_manager.BoidManager):
        uut = app.RestfulApi(default_simulation, small_world, default_boid_manager)
        result = uut.api_v1_get_simulation()

        assert result.state == default_simulation.state
        assert result.rate == default_simulation.rate
        assert len(default_simulation.next_states)
        for n in default_simulation.next_states:
            assert n in result.next_states

    def test_api_v1_put_simulation(self,
                                   default_simulation: simulation.SimulationManager,
                                   small_world: simulation.world.World,
                                   default_boid_manager: simulation.boid_manager.BoidManager):
        desired_state = boidsapi.boids.SimulationState.RUNNING
        desired_rate = 5.0

        uut = app.RestfulApi(default_simulation, small_world, default_boid_manager)
        request = boidsapi.boids.SimulationControlUpdateRequest(desired_state,
                                                                desired_rate)
        result = uut.api_v1_put_simulation(request.to_dict())

        assert default_simulation.state == desired_state
        assert default_simulation.rate == desired_rate
        assert result.state == default_simulation.state
        assert result.rate == default_simulation.rate
        assert len(default_simulation.next_states)
        for n in default_simulation.next_states:
            assert n in result.next_states

    def test_api_v1_put_simulation_bad_request(self,
                                               default_simulation: simulation.SimulationManager,
                                               small_world: simulation.world.World,
                                   default_boid_manager: simulation.boid_manager.BoidManager):
        uut = app.RestfulApi(default_simulation, small_world, default_boid_manager)

        # Should have either state or rate, but this request is empty
        request = boidsapi.boids.SimulationControlUpdateRequest()

        with pytest.raises(werkzeug.exceptions.BadRequest):
            uut.api_v1_put_simulation(request.to_dict())

    def test_api_v1_get_config(self,
                               default_simulation: simulation.SimulationManager,
                               small_world: simulation.world.World,
                               default_boid_manager: simulation.boid_manager.BoidManager):
        uut = app.RestfulApi(default_simulation, small_world, default_boid_manager)
        result: boidsapi.boids.SimulationConfigStatus = uut.api_v1_get_config()

        assert result.world_config.current.width == small_world.width
        assert result.world_config.current.height == small_world.height
        assert result.world_config.defaults.width == small_world.defaults['width']
        assert result.world_config.defaults.height == small_world.defaults['height']
        assert result.world_config.limits.width.min == small_world.limits['width']['min']
        assert result.world_config.limits.width.max == small_world.limits['width']['max']
        assert result.world_config.limits.height.min == small_world.limits['height']['min']
        assert result.world_config.limits.height.max == small_world.limits['height']['max']

        boidsapi.boids.SimulationConfigStatus.from_dict(result.to_dict())

    def test_api_v1_put_config(self,
                               default_simulation: simulation.SimulationManager,
                               small_world: simulation.world.World,
                               default_boid_manager: simulation.boid_manager.BoidManager):
        uut = app.RestfulApi(default_simulation, small_world, default_boid_manager)

        world_update = boidsapi.boids.WorldConfig(width=200, height=456)
        boids_update = boidsapi.boids.BoidsConfig(quantity=42,
                                                  avoid_walls=False,
                                                  view_range=33,
                                                  view_angle=152,
                                                  speed_limits=boidsapi.boids.IntegerRange(3, 33))

        result: boidsapi.boids.SimulationConfigStatus = uut.api_v1_put_config(boidsapi.boids.SimulationConfigUpdateRequest(world_config=world_update,
                                                                                                                           boids_config=boids_update).to_dict())

        assert result.world_config.current.width == world_update.width
        assert result.world_config.current.height == world_update.height
        assert result.boids_config.current.avoid_walls == boids_update.avoid_walls