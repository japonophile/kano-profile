#!/usr/bin/env python

import time
import atexit
from kano.utils import get_program_name, is_number
from kano_profile.apps import load_app_state_variable, save_app_state_variable, save_app_state


class Tracker:
    def __init__(self):
        self.start_time = time.time()
        self.program_name = get_program_name()
        atexit.register(self.write_times)

    def calculate_elapsed(self):
        return time.time() - self.start_time

    def write_times(self):
        add_runtime_to_app(self.program_name, self.calculate_elapsed())


def add_runtime_to_app(app, runtime):
    if not app:
        return

    if not is_number(runtime):
        return

    runtime = float(runtime)

    app = app.replace('.', '_')

    state = load_app_state_variable('kano-tracker', app)

    try:
        state['starts'] += 1
        state['runtime'] += runtime
    except Exception:
        state = {
            'starts': 1,
            'runtime': runtime,
        }

    save_app_state_variable('kano-tracker', app, state)


def save_hardware_info():
    from kano.logging import logger
    from kano.utils import get_cpu_id, get_mac_address, detect_kano_keyboard

    logger.info('save_hardware_info')
    state = {
        'cpu_id': get_cpu_id(),
        'mac_address': get_mac_address(),
        'kano_keyboard': detect_kano_keyboard(),
    }
    save_app_state('kano-hardware', state)