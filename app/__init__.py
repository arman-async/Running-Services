import logging

from app.config import Logger as config

logger = logging.getLogger(__name__)
formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(config.LOG_FILE, mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(config.LOG_LEVEL)

logger.info('App Initialized')