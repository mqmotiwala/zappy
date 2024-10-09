import os
import json
from helpers.logger import setup_logger, logger

class StateMachine:
    STATE_FILE = 'zappy_state.json'
    DEFAULT_ZAPPED_STATUS = False
    STATE_MACHINE_ZAPPED_STATUS_KEY = 'zapped_today'

    def __init__(self, root):
        self.state_file_path = os.path.join(root, self.STATE_FILE)
        self.current_state = self.load_state()
        self.zapped_today = self.current_state.get(self.STATE_MACHINE_ZAPPED_STATUS_KEY, self.DEFAULT_ZAPPED_STATUS)

    def load_state(self):
        if os.path.exists(self.state_file_path):
            with open(self.state_file_path, 'r') as file:
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
        with open(self.state_file_path, 'w') as file:
            json.dump(state, file)

if __name__ == '__main__':
    """
        this will execute only when the script is ran directly
        cron will run this script daily at midnight, resetting the state
    """

    # get reference to root folder for absolute path of project files
    root = os.path.dirname(__file__)

    setup_logger(root)
    s = StateMachine(root)

    s.update_state(False)
