import utils
import geometry
import itertools
import logging
import numbers
import simulation.time
import uuid
import whistle

class Boid:

    def __init__(self,
                 position: geometry.Point,
                 velocity: geometry.Vector):
        self._id = str(uuid.uuid4())

        self.logger = logging.getLogger('Boid')
        self.position = position
        self.velocity = velocity

        utils.EventBus.dispatch(BoidCreatedEvent.EVENT_NAME,
                                BoidCreatedEvent(self))

    @property
    def id(self) -> str:
        return self._id

    @property
    def velocity(self) -> geometry.Vector:
        return self._velocity

    @velocity.setter
    def velocity(self, value: geometry.Vector):
        self._velocity = value

    def update(self, velocity, position):
        self.velocity = velocity
        self.position = position
        utils.EventBus.dispatch(BoidUpdatedEvent.EVENT_NAME,
                                BoidUpdatedEvent(self))

    def __str__(self):
        return '{id:03d}: Position: {p}, Velocity: {v}'.format(id=self._id, p=self.position, v=self.velocity)

class BoidUpdatedEvent(whistle.Event):

    EVENT_NAME='boid.updated'

    def __init__(self, value: Boid) -> None:
        super().__init__()
        self.value = value

class BoidCreatedEvent(BoidUpdatedEvent):

    EVENT_NAME='boid.created'

    def __init__(self, value: Boid) -> None:
        super().__init__(value)
