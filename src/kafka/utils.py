''' This module provides Kafka-related convenience utilities '''
import logging

_logger = logging.getLogger('kafka.utils')

def to_kafka_config(config: dict[str, any]) -> dict[str, str]:
    ''' Converts a given Python dict to a Kafka-compliant configuration '''
    try:
        return {
            'bootstrap.servers': ','.join(config['bootstrap.servers'])
        }
    except KeyError as ex:
        _logger.error(f'Missing required configuration value: {ex}')
        raise
