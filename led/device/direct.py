from typing import Dict, List

from led.led import LED
from led.gpio import GPIO
from led.logging import logger

leds: Dict[str, LED]


def initialize(options: Dict):
    leds = {}
    GPIO.setmode(GPIO.BCM)
    for item in options['leds']:
        led = LED(
           name=item['name'],
            pin=item['pin'],
            state=False
        )
        GPIO.setup(led.pin, GPIO.OUT)
        GPIO.output(led.pin, GPIO.LOW)
        leds[item['name']] = led


def turn_on(led_name: str):
    logger.debug(f"Turning ON LED named {led_name}")
    GPIO.output(leds[led_name], GPIO.HIGH)


def turn_off(led_name: str):
    logger.debug(f"Turning OFF LED named {led_name}")
    GPIO.output(leds[led_name], GPIO.LOW)


def cleanup():
    GPIO.cleanup()