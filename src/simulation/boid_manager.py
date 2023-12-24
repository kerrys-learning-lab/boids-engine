''' Manages all of the Boids in the world '''
import numbers
import random
import typing
import system
import boidsapi.boids
import simulation.behaviors
import simulation.behaviors.behavior_manager
import simulation.boids.boid
import simulation.boids.traits
import simulation.world
import geometry
import utils

class Neighbors:
    ''' Allows pair-wise comparison of two Boids. '''

    def __init__(self,
                 boid_one: simulation.boids.boid.Boid,
                 boid_two: simulation.boids.boid.Boid,
                 view_angle,
                 view_range):
        self.view_angle = view_angle
        self.view_range = view_range
        self.boid_one = boid_one
        self.boid_two = boid_two
        self.vector_b1_to_b2 = geometry.Vector.fromPoints(boid_one.position, boid_two.position)

    def is_neighbor_visible(self):
        ''' Returns true if boid_two is visible from boid_one's perspective,
            accounting for boid_one's field-of-view and line-of-sight
            (distance only)'''
        left_limit = self.boid_one.velocity.angleXY - (self.view_angle / 2)
        right_limit = left_limit + self.view_angle

        if self.vector_b1_to_b2.magnitude < self.view_range:
            return left_limit <= self.vector_b1_to_b2.angleXY <= right_limit

        return False


class BoidManager(simulation.boids.traits.Traits):
    ''' Manages all of the Boids in the world. '''

    def __init__(self,
                 world: 'simulation.world.World',
                 config: dict) -> None:
        super().__init__(config)
        self._boids: typing.List[simulation.boids.boid.Boid] = []
        self._behaviors = simulation.behaviors.behavior_manager.BehaviorManager(self)
        self._world = world
        self._neighbors = None

    def append(self, value: simulation.boids.boid.Boid = None):
        ''' Adds the given Boid for management.  If no Boid is specified, a
            Boid is created at a random location within the world and is given
            a random velocity '''
        if value is None:
            random_position = BoidManager.RandomPosition(self._world.width,
                                                         self._world.height)
            random_velocity = BoidManager.RandomVelocity(self._speed_limits)
            value = simulation.boids.boid.Boid(position=random_position,
                                               velocity=random_velocity)
        self._boids.append(value)
        self._logger.info(f'Created new Boid: {value.id}')

    def __add__(self, value: simulation.boids.boid.Boid):
        self.append(value)


    def __len__(self) -> numbers.Number:
        return self.quantity

    def update(self, timestamp: boidsapi.boids.SimulationTimestamp):
        ''' Updates each Boid's position given delta_time '''
        for boid_iter in self._boids:
            vel, pos = self._behaviors.apply(timestamp.delta_time, boid_iter, self._world)
            boid_iter.update(vel, pos)

    @property
    def quantity(self) -> numbers.Number:
        return len(self._boids)

    @quantity.setter
    def quantity(self, value: numbers.Number):
        previous_qty = self.quantity

        while self.quantity < value:
            self.append()
        self._boids = self._boids[:value]

        if previous_qty != self.quantity:
            system.Log(system.SystemEventLevel.INFO,
                       f'Number of Boids: {self.quantity}')

    def on_normalize_velocity_change(self, value):
        ''' Adjusts behaviors depending on whether 'normalize_velocity' is
            True or False '''
        if value:
            self._behaviors += simulation.behaviors.NormalizeVelocity(self)
        else:
            self._behaviors.remove_by_class(simulation.behaviors.NormalizeVelocity)

    def on_avoid_walls_change(self, value):
        ''' Adjusts behaviors depending on whether 'avoid_walls' is True or
            False '''
        if value:
            self._behaviors += simulation.behaviors.NorthWallAvoider(self)
            self._behaviors += simulation.behaviors.SouthWallAvoider(self)
            self._behaviors += simulation.behaviors.EastWallAvoider(self)
            self._behaviors += simulation.behaviors.WestWallAvoider(self)
        else:
            self._behaviors.remove_by_tag(simulation.behaviors.WALL_AVOIDANCE_TAG)


    @property
    def neighbors(self) -> typing.Dict[numbers.Number, typing.List[Neighbors]]:
        if self._neighbors is None:
            self._neighbors = {}
            for i in range(len(self._boids) - 1):
                for k in range(i + 1, len(self._boids)):
                    b1 = self._boids[i]
                    b2 = self._boids[k]

                    pair1 = Neighbors(b1, b2, self.view_angle_radians, self.view_range)
                    pair2 = Neighbors(b2, b1, self.view_angle_radians, self.view_range)
                    if pair1.vector_b1_to_b2.magnitude <= self.view_range:
                        self._neighbors.get(b1.id, []).append(pair1)
                    if pair2.vector_b1_to_b2.magnitude <= self.view_range:
                        self._neighbors.get(b2.id, []).append(pair2)

        return self._neighbors


    @ staticmethod
    def RandomPosition(width, height):
        ''' Generates a random position that lies within the World's
            specified boundaries '''
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        return geometry.Vector(x, y)

    @ staticmethod
    def RandomVelocity(speed_range: utils.Range):
        ''' Generates a random velocity that complies with the
            configured World parameters '''
        return geometry.Vector(speed_range.random(allow_negative=True),
                               speed_range.random(allow_negative=True))
