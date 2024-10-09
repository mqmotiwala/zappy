import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from logger import logger

class Database:

    DB_NAME = 'zaps.db'
    DEFAULT_ACTION = "zap_detected"
    PREFERRED_TIMEZONE = 'America/Los_Angeles' #PST timezone
    PREFERRED_DATE_FORMAT = '%Y-%m-%d'
    PREFERRED_TIME_FORMAT = '%H:%M:%S'

    def __init__(self, root):
        self.db_path = os.path.join(root, self.DB_NAME)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS zaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                action TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def log_zap(self, action=None):
        if not action:
            action = self.DEFAULT_ACTION

        logger.debug(f"writing action={action} to {self.DB_NAME}")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        current_time = datetime.now(ZoneInfo(self.PREFERRED_TIMEZONE))
        date_str = current_time.strftime(self.PREFERRED_DATE_FORMAT)
        time_str = current_time.strftime(self.PREFERRED_TIME_FORMAT)

        cursor.execute('''
            INSERT INTO zaps (date, time, action)
            VALUES (?, ?, ?)
        ''', (date_str, time_str, action))

        conn.commit()
        conn.close()