import requests
import datetime
import traceback

import os
from dotenv import load_dotenv
from logger import logger

class Pushover:
    HEADERS = {'Content-Type': 'application/json'}
    PUSHOVER_URL = 'https://api.pushover.net/1/messages.json'

    def __init__(self):
        load_dotenv()

        self.user = os.getenv('PUSHOVER_USER')
        self.zappy_token = os.getenv('PUSHOVER_ZAPPY_TOKEN')
        self.logs_token = os.getenv('PUSHOVER_LOGS_TOKEN')
        self.app_name = 'Zappy'

        if not self.user or not self.zappy_token or not self.logs_token:
            logger.error("One or more required environment variables are missing.")
            raise ValueError("Missing environment variables for Pushover configuration.")

    def send_notification(self, msg, priority=0, is_log=False):
        """
        Make an API call to Pushover.

        Args:
            msg (str): The message text to be sent via Pushover.
            priority (int): Notification priority, as defined by the Pushover API specification.
            is_log (bool): If True, the notification is sent to the Logs project using PUSHOVER_LOGS_TOKEN.
                        Otherwise, it is logged to the Zappy project using PUSHOVER_ZAPPY_TOKEN.
        """

        params = {
            'title': self.app_name,
            'token': self.logs_token if is_log else self.zappy_token,
            'user': self.user,
            'message': msg,
            'priority': priority
        }

        try:
            requests.post(self.PUSHOVER_URL, json=params, headers=self.HEADERS)
            logger.info(f"Notification sent successfully. msg = {msg}")
        except Exception as e:
            logger.exception("An error occurred while sending a notification to Pushover")