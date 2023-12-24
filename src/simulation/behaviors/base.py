import logging

DELTA_V_INCR = 0.0001

EARLY_ORDER = 0
MED_ORDER = 50
LATE_ORDER = 100

COLLISION_AVOIDANCE_TAG = 'collision-avoidance'
WALL_AVOIDANCE_TAG = 'wall-avoidance'
SPEED = 'speed'


class Behavior:

    def __init__(self, order, tags):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.order = order
        self.tags = tags

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self._order = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if not hasattr(self, '_tags'):
            self._tags = []
        value = value if type(value) is list else [value]
        for t in value:
            if t not in self._tags:
                self._tags.append(t)
