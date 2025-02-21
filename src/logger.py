import logging
from logging.config import dictConfig

from src.log_config import dict_config

dictConfig(dict_config)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
