import logging
from logging.config import dictConfig

from src.log_config import dict_config

# Инициализация конфигурации логгера
dictConfig(dict_config)


def get_logger(name: str = "root") -> logging.Logger:
    """
    Получить логгер по имени. Если имя не указано, используется логгер по умолчанию (root).

    :param name: Имя логгера. По умолчанию используется "root".
    :return: Логгер с заданным именем.
    """
    return logging.getLogger(name)
