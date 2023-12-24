import datetime
import numbers
import typing
import utils
import whistle
import boidsapi.boids

class TickEvent(whistle.Event):
    EVENT_NAME='boids.tick-event'

    def __init__(self, timestamp: boidsapi.boids.SimulationTimestamp) -> None:
        super().__init__()
        self.timestamp = timestamp

class SimulationClock:

    def __init__(self):
        self._timestamp = boidsapi.boids.SimulationTimestamp()
        self._elapsed_time = None
        self.reset()

    def reset(self):
        self._elapsed_time = datetime.timedelta()
        self._timestamp.tick = 0

    @property
    def rate(self):
        return self._timestamp.delta_time

    @rate.setter
    def rate(self, value):
        self._timestamp.delta_time = value


    def tick(self):
        self._elapsed_time += datetime.timedelta(seconds=self._timestamp.delta_time)
        self._timestamp.tick += 1
        utils.EventBus.dispatch('tick', TickEvent(self.timestamp))

    @property
    def timestamp(self):
        total_seconds = self._elapsed_time.seconds
        millis = int(self._elapsed_time.microseconds / 1000)

        hours = total_seconds // 3600
        minutes = total_seconds % 3600 // 60
        seconds = total_seconds % 60

        self._timestamp.elapsed_time = f'{hours:02}:{minutes:02}:{seconds:02}.{millis:03}'
        return self._timestamp

clock = SimulationClock()
