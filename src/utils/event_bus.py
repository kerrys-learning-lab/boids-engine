import functools
import whistle

class EventBus:

    DISPATCHER = whistle.EventDispatcher()

    @staticmethod
    def dispatch(event_id, event=None):
        EventBus.DISPATCHER.dispatch(event_id, event=event)

    @staticmethod
    def add_listener(event_id, listener, priority=0):
        EventBus.DISPATCHER.add_listener(event_id, listener, priority)

    @staticmethod
    def listen(event_id, priority=0):
        ''' Function decorator '''
        def wrapper(free_function):
            EventBus.DISPATCHER.add_listener(event_id, free_function, priority)
            return free_function

        return wrapper

