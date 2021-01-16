from importlib import import_module
from typing import Dict

modules = {"direct": "direct"}

active_device = None
_active_module = None

cleanup: callable
turn_on: callable
turn_off: callable


def initialize(device_name: str, device_options: Dict):
    global _active_module
    methods = ["cleanup", "turn_off", "turn_on"]
    module_name = modules[device_name]
    _active_module = import_module(f"led.device.{module_name}")
    getattr(_active_module, "initialize")(device_options)
    for method_name in methods:
        globals()[method_name] = getattr(_active_module, method_name)
