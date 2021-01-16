from typing import Dict, List

from led.led import LED
from led.gpio import GPIO
from led.logging import logger

leds: Dict[str, LED]


def initialize(options: Dict):
    global leds
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
    global leds
    logger.debug(f"Turning ON LED named {led_name}")
    GPIO.output(leds[led_name].pin, GPIO.HIGH)
    leds[led_name].state = True


def turn_off(led_name: str):
    global leds
    logger.debug(f"Turning OFF LED named {led_name}")
    GPIO.output(leds[led_name].pin, GPIO.LOW)
    leds[led_name].state = False


def cleanup():
    GPIO.cleanup()