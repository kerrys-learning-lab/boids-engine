import app
import simulation
import simulation.boid_manager
import simulation.world
import pytest


@pytest.fixture
def small_world():
    return simulation.world.World({
        'defaults': {
            'width': 160,
            'height': 120
        },
        'limits': {
            'width': {
                'min': 160,
                'max': 1200
            },
            'height': {
                'min': 120,
                'max': 900
            }
        }
    })

@pytest.fixture
def default_restfulapi(default_simulation, small_world):
    return app.RestfulApi(default_simulation, small_world)

@pytest.fixture
def default_boid_manager(small_world: simulation.world.World) -> simulation.boid_manager.BoidManager:
    return simulation.boid_manager.BoidManager(small_world, {
        'defaults': {
            'quantity': 0,
            'avoid_walls': True,
            'normalize_velocity': True,
            'view_range': 75,
            'view_angle': 120,
            'collision_avoidance_range': 75,
            'speed_limits': {
                'min': 1,
                'max': 60
            },
            'collision_avoidance_weight': 0.3,
            'velocity_matching_weight': 0.5,
            'velocity_normalization_weight': 0.5,
            'flock_centering_weight': 0.5
        },
        'limits': {
            'quantity': {
                'min':   0,
                'max': 100
            },
            'view_range': {
                'min':   1,
                'max': 250
            },
            'view_angle': {
                'min':   0,
                'max': 359
            },
            'speed_limits': {
                'min':   1,
                'max': 100
            }
        }
    })


@pytest.fixture
def default_simulation(small_world: simulation.world.World, default_boid_manager: simulation.boid_manager.BoidManager):
    return simulation.SimulationManager(small_world, default_boid_manager)
