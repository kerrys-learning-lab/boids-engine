import enum
import logging
import numbers
import boidsapi.boids


class RangeClusterType(enum.Enum):
    NONE = 0
    DBSCAN = 1
    TILE = 2
    DBSCAN_W_TILE = 3

    def createAlgorithm(self, config):
        if self.name == 'NONE':
            return NoRangeClustering(config)
        else:
            import clustering  # no-pep8
            if self.name == 'DBSCAN':
                return clustering.DBSCAN(config)
            elif self.name == 'TILE':
                return clustering.Tile(config)
            elif self.name == 'DBSCAN_W_TILE':
                return clustering.DBSCANwithTile(config)


class World(object):

    def __init__(self, config):
        self._logger = logging.getLogger(self.__class__.__name__)
        try:
            self._defaults = config['defaults']
            self._limits = config['limits']
            self._width = self._defaults['width']
            self._height = self._defaults['height']
        except KeyError as ex:
            self._logger.error(f'Missing required configuration value: {ex}')
            raise
        # self._range_cluster_algorithm = World.CREATE_RANGE_CLUSTER_ALGORITHM(config.get('range_cluster_type', World.DEFAULT_CONFIG['range_cluster_type']),
        #                                                                      config.get('range_cluster_options', World.DEFAULT_CONFIG['range_cluster_options']))

    # @property
    # def range_cluster_type(self) -> RangeClusterType:
    #     return self._range_cluster_type

    # @range_cluster_type.setter
    # def range_cluster_type(self, value: typing.Union[RangeClusterType, str]):
    #     self._range_cluster_type = RangeClusterType[value] if type(value) is str else value

    # @property
    # def range_cluster_options(self) -> dict:
    #     return self._range_cluster_options

    # @range_cluster_options.setter
    # def range_cluster_options(self, value: dict):
    #     self._range_cluster_options = value

    @property
    def defaults(self) -> dict:
        return self._defaults

    @property
    def limits(self) -> dict:
        return self._limits

    @property
    def width(self) -> numbers.Number:
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self) -> numbers.Number:
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def update(self, timestamp: boidsapi.boids.SimulationTimestamp):
        pass

    @staticmethod
    def CREATE_RANGE_CLUSTER_ALGORITHM(value, options):
        value: RangeClusterType = RangeClusterType[value] if type(value) is str else value
        return value.createAlgorithm(options)


class NoRangeClustering(object):

    def __init__(self, config={}):
        pass

    def __call__(self, world: World):
        pass
        # for i in range(0, len(world.boids)-1):
        #     for k in range(i+1, len(world.boids)):
        #         v = geometry.Vector.fromPoints(world.boids[k].position, world.boids[i].position)
        #         if v.magnitude < world.boidConfig.get('range'):
        #             if world.boids[i].angleBetweenBoids(v) < world.boids[i].view_angle:
        #                 world.boids[i].boid_mask[k] = 1
        #             if world.boids[k].angleBetweenBoids(v) < world.boids[k].view_angle:
        #                 world.boids[k].boid_mask[i] = 1
