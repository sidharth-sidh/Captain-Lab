import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def create_logger(log_path=None):
    target = Path(log_path) if log_path else Path(__file__).resolve().parents[1] / "logs" / "agent.log"
    target.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("lab-management-agent")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler = RotatingFileHandler(str(target), maxBytes=2 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger
