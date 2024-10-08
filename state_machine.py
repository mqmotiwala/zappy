import os
import json
from helpers.logger import logger

class StateMachine:
    STATE_FILE = 'zappy_state.json'
    DEFAULT_ZAPPED_STATUS = False
    STATE_MACHINE_ZAPPED_STATUS_KEY = 'zapped_today'

    def __init__(self):
        self.current_state = self.load_state()
        self.zapped_today = self.current_state.get(self.STATE_MACHINE_ZAPPED_STATUS_KEY, self.DEFAULT_ZAPPED_STATUS)

    def load_state(self):
        if os.path.exists(self.STATE_FILE):
            with open(self.STATE_FILE, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    logger.error("Failed to decode state file, resetting state.")
                    return {}
        return {}

    def update_state(self, zapped_today):
        state = {
            self.STATE_MACHINE_ZAPPED_STATUS_KEY: zapped_today
        }

        logger.debug(f"Zappy state set to {zapped_today}")
        with open(self.STATE_FILE, 'w') as file:
            json.dump(state, file)

if __name__ == '__main__':
    """
        this will execute only when the script is ran directly
        cron will run this script daily at midnight, resetting the state
    """

    s = StateMachine()
    s.update_state(False)
