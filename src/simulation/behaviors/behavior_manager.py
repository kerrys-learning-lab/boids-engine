''' Manages Boid behavior '''
import logging
import typing
import simulation.behaviors.base
import simulation.behaviors.constrain_velocity
import simulation.behaviors.constrain_position
import simulation.boids.boid
import simulation.boids.traits
import simulation.world

class BehaviorManager:
    ''' Manages Boid behavior '''

    def __init__(self, boids_traits: simulation.boids.traits.Traits):
        self._boids_traits = boids_traits
        self.behaviors: typing.List[simulation.behaviors.base.Behavior] = []
        self.logger = logging.getLogger(self.__class__.__name__)
        self._velocity_constraint = simulation.behaviors.constrain_velocity.ConstrainVelocity(boids_traits)
        self._position_constraint = simulation.behaviors.constrain_position.ConstrainPosition(boids_traits)

    def __iadd__(self, b: simulation.behaviors.base.Behavior):
        self.logger.info('Adding Behavior: {b} (Tags = {t})'.format(b=b.__class__.__name__,
                                                                    t=', '.join(b.tags)))
        self.behaviors.append(b)
        self.behaviors = sorted(self.behaviors, key=lambda b: b.order)
        return self

    def remove_by_tag(self, t):
        ''' Removes all Behaviors which are tagged with 't' '''
        before = len(self.behaviors)
        self.behaviors = [b for b in self.behaviors if t not in b.tags]
        self.logger.debug('Removed behaviors by tag "{t}".  Length before: {b}, after: {a}'.format(t=t,
                                                                                                   b=before,
                                                                                                   a=len(self.behaviors)))

    def remove_by_class(self, c):
        ''' Removes Behavior of type 'c' '''
        before = len(self.behaviors)
        self.behaviors = [b for b in self.behaviors if b.__class__.__name__ != c.__name__]
        self.logger.debug('Removed behaviors by class "{c}".  Length before: {b}, after: {a}'.format(c=c.__name__,
                                                                                                     b=before,
                                                                                                     a=len(self.behaviors)))

    def apply(self, delta_time, boid:simulation.boids.boid.Boid, world: simulation.world.World):
        ''' Applies behaviors to the given Boid '''
        velocity = boid.velocity.clone()
        position = boid.position.clone()

        for behavior in self.behaviors:
            velocity += behavior(delta_time, boid, world)

        velocity = self._velocity_constraint(delta_time, boid, world, velocity)
        position += velocity * delta_time
        position = self._position_constraint(delta_time, boid, world, position)

        return velocity, position
