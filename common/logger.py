import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

_project_root = Path(__file__).resolve().parents[1]
_log_dir = _project_root / ".logs"
_log_dir.mkdir(parents=True, exist_ok=True)
_log_file = _log_dir / "app.log"

if not logger.handlers:
    # 파일 핸들러
    file_handler = TimedRotatingFileHandler(
        str(_log_file), when="midnight", backupCount=30, encoding="utf-8"
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