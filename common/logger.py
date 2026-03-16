import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# 파일 핸들러
file_handler = TimedRotatingFileHandler(
    'app.log', when='midnight', backupCount=30, encoding='utf-8'
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# 콘솔 핸들러
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def info(msg):
    logger.info(msg)

def error(msg):
    logger.error(msg)

def debug(msg):
    logger.debug(msg)

def warning(msg):
    logger.warning(msg)

def critical(msg):
    logger.critical(msg)