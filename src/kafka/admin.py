''' This module provides utilities to administer Kafka '''
import logging
import confluent_kafka
import confluent_kafka.admin
from . import utils
import time

class TopicExists(RuntimeError):
    ''' Raised upon the attempt to create a Kafka topic which already exists'''
    pass

class AdminClient:
    ''' Administers a Kakfa instance '''
    TOPIC_CREATION_DELAY_SECONDS = 30

    def __init__(self, config: dict[str, any]) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        config = utils.to_kafka_config(config)
        self._impl = confluent_kafka.admin.AdminClient(config)

    def create(self, config: dict[str, any]):
        ''' Creates Kafka elements from the given configuration.  Currently,
            only topic creation is supported. '''
        for topic_name, topic_config in config.get('topics', {}).items():
            num_partitions = topic_config.pop('num_partitions')
            self.create_topic(topic_name, num_partitions, topic_config)

    def create_topic(self, topic_name: str, num_partitions: int, topic_config: dict):
        try:
            self._logger.debug(f'Creating topic {topic_name}')
            topic = confluent_kafka.admin.NewTopic(topic_name,
                                                   num_partitions,
                                                   config=topic_config)

            self.verify_topic(topic_name, invert=True)
            self._impl.create_topics([topic])
            self._logger.info(f'Created topic {topic_name}')
            self._logger.debug(f"By observation, it can take up to ~{AdminClient.TOPIC_CREATION_DELAY_SECONDS}s for a newly created topic to 'settle'")
            time.sleep(AdminClient.TOPIC_CREATION_DELAY_SECONDS)
            self._logger.debug(f"Verifying successful creation of topic '{topic_name}'")
            self.verify_topic(topic_name)
        except TopicExists:
            self._logger.info(f'Topic "{topic_name}" already exists')
        except confluent_kafka.KafkaException as ex:
            self._process_kafka_exception(ex)
        except KeyError as ex:
            self._logger.error(f'Topic "{topic_name}" is missing required attribute: {ex}')

    def verify_topic(self, topic_name, invert=False):
        try:
            resource = confluent_kafka.admin.ConfigResource(confluent_kafka.admin.ConfigResource.Type.TOPIC,
                                                            topic_name)
            # all_results = self._impl.describe_configs([resource])
            # for _, config_resource_future in all_results.items():
            #     for config_name, config_entry in config_resource_future.result().items():
            #         self._logger.debug(f'{topic_name}/{config_name}: {config_entry.value}')

            if invert:
                raise TopicExists()

        except confluent_kafka.KafkaException as ex:
            if not invert:
                self._process_kafka_exception(ex)

    def remove_topics(self, topic_list):
        all_results = self._impl.delete_topics(topic_list)
        for topic_name, topic_delete_future in all_results.items():
            try:
                topic_delete_future.result()
                self._logger.info(f'Removed topic: {topic_name}')
            except confluent_kafka.KafkaException as ex:
                error: confluent_kafka.KafkaError = ex.args[0]
                if error.code() == confluent_kafka.KafkaError.UNKNOWN_TOPIC_OR_PART:
                    self._logger.warn(f'Unknown topic: {topic_name}')
                else:
                    self._process_kafka_exception(ex)

    def _process_kafka_exception(self, ex):
        error: confluent_kafka.KafkaError = ex.args[0]
        self._logger.error(f'Unexpected Kafka error: {error.str()}')
        raise ex
