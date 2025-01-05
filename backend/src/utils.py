"""
This file include useful tools.

- logger
- recursive search
"""

from os.path import isfile
from logging.handlers import RotatingFileHandler

from loguru import logger
from config import config

if not isfile(config.log_path):
    with open(config.log_path, mode='w', encoding="utf-8") as f:
        pass

handler = RotatingFileHandler(
    config.log_path,
    maxBytes=5000000,
    backupCount=6,
)

logger.add(handler)
