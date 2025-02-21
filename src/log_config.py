import sys
from pathlib import Path

# Путь для хранения логов
log_folder_path = Path(__file__).parent.parent / "logs"
log_folder_path.mkdir(exist_ok=True)
log_file_path = log_folder_path / "logfile.log"

# Конфигурация логгера
dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "fileFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z",
        },
        "consoleFormatter": {
            "format": "%(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "stream": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "consoleFormatter",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "fileFormatter",
            "filename": str(log_file_path),
            "maxBytes": 10 ** 6,
            "backupCount": 5,
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["stream", "file"],
    },
}
