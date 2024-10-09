import sys
import logging

LOG_FILE = 'zappy.log'
DEFAULT_STREAM_LOG_LEVEL = 'DEBUG'
DEFAULT_FILE_LOG_LEVEL = 'DEBUG'

sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

preferred_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(getattr(logging, DEFAULT_STREAM_LOG_LEVEL))
stream_handler.setFormatter(preferred_format)

file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(getattr(logging, DEFAULT_FILE_LOG_LEVEL))
file_handler.setFormatter(preferred_format)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)