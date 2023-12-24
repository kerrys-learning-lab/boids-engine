import numbers
import logging
import math
import utils


class Traits:

    def __init__(self,
                 config: dict) -> None:
        self._defaults = config['defaults']
        self._limits = config['limits']
        self._logger = logging.getLogger(self.__class__.__name__)

        try:
            self._view_range = self._defaults['view_range']
            self._view_angle = self._defaults['view_angle']
            self._view_angle_radians = math.radians(self._view_angle)
            self._collision_avoidance_range = self._defaults['collision_avoidance_range']
            self._collision_avoidance_weight = self._defaults['collision_avoidance_weight']
            self._velocity_matching_weight = self._defaults['velocity_matching_weight']
            self._normalize_velocity = self._defaults['normalize_velocity']
            self._velocity_normalization_weight = self._defaults['velocity_normalization_weight']
            self._flock_centering_weight = self._defaults['flock_centering_weight']
            self._speed_limits = utils.Range(**self._defaults['speed_limits'])
            self._avoid_walls = self._defaults['avoid_walls']
        except KeyError as ex:
            self._logger.error(f'Missing required configuration value: {ex}')
            raise

    @property
    def defaults(self) -> dict:
        return self._defaults

    @property
    def limits(self) -> dict:
        return self._limits

    @property
    def view_range(self) -> numbers.Number:
        return self._view_range

    @view_range.setter
    def view_range(self, value: numbers.Number):
        if self.view_range != value:
            self._view_range = value
            self._invoke_on_change('view_range', self.view_range)

    @property
    def collision_avoidance_range(self):
        return self._collision_avoidance_range

    @collision_avoidance_range.setter
    def collision_avoidance_range(self, value):
        if self.collision_avoidance_range != value:
            self._collision_avoidance_range = value
            self._invoke_on_change('collision_avoidance_range', self.collision_avoidance_range)

    @property
    def collision_avoidance_weight(self):
        return self._collision_avoidance_weight

    @collision_avoidance_weight.setter
    def collision_avoidance_weight(self, value):
        if self.collision_avoidance_weight != value:
            self._collision_avoidance_weight = value
            self._invoke_on_change('collision_avoidance_weight', self.collision_avoidance_weight)

    @property
    def velocity_matching_weight(self):
        return self._velocity_matching_weight

    @velocity_matching_weight.setter
    def velocity_matching_weight(self, value):
        if self.velocity_matching_weight != value:
            self._velocity_matching_weight = value
            self._invoke_on_change('velocity_matching_weight', self.velocity_matching_weight)

    @property
    def normalize_velocity(self):
        return self._normalize_velocity

    @normalize_velocity.setter
    def normalize_velocity(self, value):
        if self.normalize_velocity != value:
            self._normalize_velocity = value
            self._invoke_on_change('normalize_velocity', self.normalize_velocity)

    @property
    def velocity_normalization_weight(self):
        return self._velocity_normalization_weight

    @velocity_normalization_weight.setter
    def velocity_normalization_weight(self, value):
        if self.velocity_matching_weight != value:
            self._velocity_normalization_weight = value
            self._invoke_on_change('velocity_matching_weight', self.velocity_matching_weight)

    @property
    def flock_centering_weight(self):
        return self._flock_centering_weight

    @flock_centering_weight.setter
    def flock_centering_weight(self, value):
        if self.flock_centering_weight != value:
            self._flock_centering_weight = value
            self._invoke_on_change('flock_centering_weight', self.flock_centering_weight)

    @property
    def wall_avoid_weight(self):
        return self._wall_avoid_weight

    @wall_avoid_weight.setter
    def wall_avoid_weight(self, value):
        if self.wall_avoid_weight != value:
            self._wall_avoid_weight = value
            self._invoke_on_change('wall_avoid_weight', self.wall_avoid_weight)

    @property
    def min_speed(self) -> numbers.Number:
        return self._speed_limits.min

    @property
    def max_speed(self) -> numbers.Number:
        return self._speed_limits.max

    @property
    def speed_limits(self) -> utils.Range:
        return self._speed_limits

    @speed_limits.setter
    def speed_limits(self, value: utils.Range):
        if self.speed_limits != value:
            self._speed_limits = value
            self._invoke_on_change('speed_limits', self.speed_limits)

    @property
    def view_angle(self):
        return self._view_angle

    @view_angle.setter
    def view_angle(self, value):
        if self.view_angle != value:
            self._view_angle = value
            self._view_angle_radians = math.radians(value)
            self._invoke_on_change('view_angle', self.view_angle)

    @property
    def view_angle_radians(self):
        return self._view_angle_radians

    @property
    def avoid_walls(self):
        return self._avoid_walls

    @avoid_walls.setter
    def avoid_walls(self, value):
        if self.avoid_walls != value:
            self._avoid_walls = value
            self._invoke_on_change('avoid_walls', self.avoid_walls)

    def _invoke_on_change(self, property_name, value):
        try:
            getattr(self, f'on_{property_name}_change')(value)
        except AttributeError:
            pass
