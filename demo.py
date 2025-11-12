from US_VISA import logger

try:
    a = 1/0
except ZeroDivisionError as e:
    logger.logging.error(e)