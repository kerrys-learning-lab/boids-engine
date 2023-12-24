import boidsapi.boids
import kafka
import kafka.topic
from simulation.boids.boid import BoidCreatedEvent, BoidUpdatedEvent
import simulation.time
import logging
import system
import kafka.utils
import utils

class BoidPublisher:

    def __init__(self, topic: kafka.topic.Topic):
        self._topic = topic
        utils.EventBus.add_listener(BoidCreatedEvent.EVENT_NAME,
                                    self.on_boid_updated_event)
        utils.EventBus.add_listener(BoidUpdatedEvent.EVENT_NAME,
                                    self.on_boid_updated_event)

    def on_boid_updated_event(self, event: BoidUpdatedEvent):
        b = boidsapi.boids.BoidTelemetryEvent(timestamp=simulation.time.clock.timestamp,
                                              level=boidsapi.boids.SystemEventLevel.TELEMETRY,
                                              event_type="BoidTelemetryEvent",
                                              id=event.value.id,
                                              position=event.value.position,
                                              velocity=event.value.velocity)
        self._topic.publish(b.to_dict())

class TimePublisher():
    def __init__(self, topic: kafka.topic.Topic):
        self._topic = topic
        utils.EventBus.add_listener(simulation.time.TickEvent.EVENT_NAME,
                                    self.on_tick_event)

    def on_tick_event(self, event: simulation.time.TickEvent):
        self._topic.publish(event.timestamp.to_dict())

class SystemEventPublisher:

    def __init__(self, topic: kafka.topic.Topic):
        self._topic = topic
        utils.EventBus.add_listener(system.SystemEvent.EVENT_NAME,
                                    self.on_system_event_event)

    def on_system_event_event(self, event: system.SystemEvent):
        b = boidsapi.boids.SystemMessageEvent(timestamp=event.timestamp,
                                              level=event.level,
                                              source=event.source,
                                              message=event.message)
        self._topic.publish(b.to_dict())

_LOGGER = logging.getLogger('kafka')

def init_publishers(config:dict):
    try:
        base_config = kafka.utils.to_kafka_config(config)

        BoidPublisher(kafka.topic.Topic('boids.boids', base_config))
        SystemEventPublisher(kafka.topic.Topic('boids.system-events', base_config))
        TimePublisher(kafka.topic.Topic('boids.system-time', base_config))
    except KeyError as ex:
        _LOGGER.error(f'Missing required configuration value: {ex}')
        raise
