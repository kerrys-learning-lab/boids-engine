import enum
import logging
import numbers
import typing
import gevent
import gevent.greenlet
import boidsapi.boids

import utils
import utils.api_utils
import system

from .boids import boid
from .boid_manager import BoidManager
from .time import clock
from .world import World

logging.getLogger("parse").setLevel(logging.WARN)
logging.getLogger("openapi_spec_validator").setLevel(logging.WARN)



class SimulationManager(gevent.greenlet.Greenlet):
    NEXT_STATES = {
        boidsapi.boids.SimulationState.PAUSED: [
            boidsapi.boids.SimulationState.RUNNING,
            boidsapi.boids.SimulationState.RESET,
            boidsapi.boids.SimulationState.STEP,
        ],
        boidsapi.boids.SimulationState.RUNNING: [boidsapi.boids.SimulationState.PAUSED],
        boidsapi.boids.SimulationState.STEP: [boidsapi.boids.SimulationState.PAUSED],
        boidsapi.boids.SimulationState.RESET: [boidsapi.boids.SimulationState.RUNNING, boidsapi.boids.SimulationState.STEP],
    }

    def __init__(
        self,
        world: World,
        boid_manager: BoidManager,
        config: dict[str, any] = {},
    ):
        gevent.greenlet.Greenlet.__init__(self)
        self._logger = logging.getLogger(self.__class__.__name__)

        self._boid_manager = boid_manager
        self._world = world
        self._tick_for = None
        self._running = False
        self._state = None

        utils.EventBus.add_listener(
            boid.BoidCreatedEvent.EVENT_NAME,
            self.on_boid_created_event,
        )

        try:
            self.state = config.get("state", boidsapi.boids.SimulationState.PAUSED)
            clock.rate = config.get("rate", 1)
        except KeyError as ex:
            self._logger.error(f"Missing required configuration value: {ex}")
            raise

    @property
    def state(self) -> boidsapi.boids.SimulationState:
        return self._state

    @state.setter
    def state(self, value: typing.Union[boidsapi.boids.SimulationState, str]):
        previous = self._state
        value = value if isinstance(value, boidsapi.boids.SimulationState) else utils.api_utils.simulationStateFromString(value)

        if value != previous:
            self._state = value
            self._logger.info("State == {s}".format(s=self.state))
            system.Log(
                system.SystemEventLevel.STATUS, f"Simulation state: {self._state}"
            )

            self.set_next_states()

    @property
    def timestamp(self):
        return clock.timestamp

    @property
    def next_states(self):
        return self._next_states

    def tick_for(self, value: numbers.Number):
        self.state = boidsapi.boids.SimulationState.STEP
        self._tick_for = value

    def _update(self):

        if self.state == boidsapi.boids.SimulationState.RUNNING or self.state == boidsapi.boids.SimulationState.STEP:

            clock.tick()

            self._world.update(clock.timestamp)
            self._boid_manager.update(clock.timestamp)

            if self._tick_for:
                self._tick_for -= 1
                self.state = (
                    boidsapi.boids.SimulationState.STEP if self._tick_for else boidsapi.boids.SimulationState.PAUSED
                )

    def stop(self):
        if self._running:
            self._running = False
            self.join()

    def _run(self):
        self._running = True
        while self._running:
            gevent.sleep(self.timestamp.delta_time)
            self._update()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def set_next_states(self):
        new_next_states = set(SimulationManager.NEXT_STATES[self.state])
        if self._boid_manager.quantity == 0:
            new_next_states.remove(boidsapi.boids.SimulationState.RUNNING)
            new_next_states.remove(boidsapi.boids.SimulationState.STEP)

        current_next_states = set(getattr(self, "_next_states", []))
        if current_next_states is None or new_next_states != current_next_states:
            self._next_states = list(new_next_states)
            self._logger.debug(f'Next states: [{", ".join(self._next_states)}]')

    def on_boid_created_event(self, event: boid.BoidCreatedEvent):
        # Boid creation may affect state (e.g. RUNNING is disabled until
        # boid quantity is > 0)
        self.set_next_states()
