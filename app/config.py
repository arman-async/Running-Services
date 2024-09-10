from dotenv import get_key

class Logger:
    LOG_FILE = get_key(".env", "LOG_FILE")
    LOG_FORMAT = get_key(".env", "LOG_FORMAT")
    LOG_LEVEL = int(get_key(".env", "LOG_LEVEL"))
 