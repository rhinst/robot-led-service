import os
from itertools import cycle
from time import sleep
from typing import Dict
import json

from redis import Redis
from redis.client import PubSub

from led.config import load_config
from led.logging import logger, initialize_logger
import led.device


def handle_turn_on(**kwargs):
    if "name" not in kwargs:
        raise ValueError("Missing argument: name")
    led.device.turn_on(kwargs['name'])


def handle_turn_off(**kwargs):
    if "name" not in kwargs:
        raise ValueError("Missing argument: name")
    led.device.turn_off(kwargs['name'])


def main():
    environment: str = os.getenv("ENVIRONMENT", "dev")
    config: Dict = load_config(environment)
    initialize_logger(level=config['logging']['level'], filename=config['logging']['filename'])
    redis_host = config['redis']['host']
    redis_port = config['redis']['port']
    logger.debug(f"Connecting to redis at {redis_host}:{redis_port}")
    redis_client: Redis = Redis(
        host=redis_host, port=redis_port, db=0
    )
    pubsub: PubSub = redis_client.pubsub(ignore_subscribe_messages=True)

    pubsub.subscribe("subsystem.led.command")
    led.device.initialize(config["device"]["name"], config["device"]["options"])
    handlers = {
        "turn_on": handle_turn_on,
        "turn_off": handle_turn_off
    }
    try:
        while cycle([True]):
            # see if there is a command for me to execute
            redis_message = pubsub.get_message()
            if redis_message is not None:
                message = json.loads(redis_message['data'])
                logger.debug(f"Received a '{message['command']}' message")
                try:
                    handlers[message["command"]](**message)
                except KeyError:
                    logger.error(f"Unrecognized command: {message['command']}")
            sleep(0.25)
    except Exception as e:
        logger.exception(f"Something bad happened: {str(e)}")
    finally:
        logger.debug("Cleaning up")
        pubsub.close()
        redis_client.close()
        led.device.cleanup()
        logger.debug("Shutting down")


if __name__ == '__main__':
    main()
