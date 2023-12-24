import logging
import uuid
import confluent_kafka
import utils

class Topic:

    def __init__(self, topic_name: str, bootstrap) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._topic_name = topic_name
        self._producer = confluent_kafka.Producer(bootstrap)

    def publish(self, value: dict, key: str =None, headers: dict[str,str] = None, callback=None):
        key = key if key else str(uuid.uuid4())
        on_delivery = callback if callback else self.default_callback

        self._producer.produce(self._topic_name,
                               value=utils.to_json(value),
                               key=key,
                               headers=headers,
                               on_delivery=on_delivery)

        # Default behavior is synchronous unless the caller provides their
        # own callback
        if callback is None:
            self._producer.flush()

    def default_callback(self, err, msg):
        if err is not None:
            self._logger.debug(f'{self._topic_name}: Error when publishing message {msg.key()}: {err}')
