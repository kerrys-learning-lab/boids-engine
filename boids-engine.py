#! /usr/bin/env python3

import argparse
import logging
import yaml
import boids_utils.config
import boids_utils.elastic
import boids_utils.logging
import boids_utils.openapi
import boids_utils.pubsub
# import boids_service.publishers
# import boids_service.server
# import boids_service.restful_api
# import simulation


LOGGER = logging.getLogger('boids-k8s-events')


# Order is important
# - utils.config *must* be first in order to load all configuration files
#   for subsequent stakeholders
# - utils.logging *should* be early in order to facilitate debugging
CLI_STAKEHOLDERS = [
    boids_utils.config,
    boids_utils.logging,
    boids_utils.elastic,
    boids_utils.openapi,
    boids_utils.pubsub,
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Boids Engine')

    for stakeholder in CLI_STAKEHOLDERS:
        stakeholder.add_cli_options(parser)

    server_group = parser.add_argument_group(title='Server options')
    server_group.add_argument('-p',
                              '--port',
                              default=9000,
                              help='Specify the server port')

    parser.add_argument('uuid',
                        nargs=1,
                        help='The SessionConfiguration UUID')

    args = parser.parse_args()

    for stakeholder in CLI_STAKEHOLDERS:
        stakeholder.process_cli_options(args, **boids_utils.config.instance)

    # try:
    #     world = simulation.world.World(config['world'])
    #     boid_manager = simulation.boid_manager.BoidManager(world, config['boids'])
    #     simulation = simulation.SimulationManager(world,
    #                                               boid_manager,
    #                                               config['simulation'])

    #     restful_api = boids_service.restful_api.RestfulApi(simulation=simulation,
    #                                                        world=world,
    #                                                        boid_manager=boid_manager)

    #     boids_service.publishers.init_publishers(config['kafka'])

    # except KeyError as ex:
    #     parser.error('Insufficient configuration data')

    # http_server = boids_service.server.createServer(restful_api,
    #                                                 port=args.port)
    # try:
    #     logger.debug('Starting simulation Greenlet...')
    #     simulation.start()

    #     logger.info(f'Starting HTTP Server listening at :{args.port}')
    #     http_server.serve_forever()
    # except KeyboardInterrupt:
    #     logger.debug('Stopping simulation Greenlet...')
    #     simulation.stop()

    #     logger.debug('Closing HTTP Server...')
    #     http_server.close()
