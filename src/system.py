import enum

import boidsapi.boids
import simulation.time
import utils
import whistle

class SystemEventLevel(str, enum.Enum):
    ERROR: str = 'ERROR'
    WARNING: str = 'WARNING'
    INFO: str = 'INFO'
    STATUS: str = 'STATUS'

class SystemEvent(whistle.Event):

    EVENT_NAME='boids.system-events'

    def __init__(self,
                 timestamp: boidsapi.boids.SimulationTimestamp,
                 level: SystemEventLevel,
                 source: str,
                 message: str):
        super().__init__()
        self.timestamp = timestamp
        self.level = level
        self.source = source
        self.message = message

def Log(level: SystemEventLevel, msg: str, source: str = 'simulation'):
    utils.EventBus.dispatch(SystemEvent.EVENT_NAME,
                            SystemEvent(simulation.time.clock.timestamp,
                                        level,
                                        source,
                                        msg))
