# datathon/core/logging_config.py
import logging
import sys
from python_json_logger import jsonlogger

def setup_logging():
    """
    Configura o sistema de logging para gerar logs em formato JSON.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logHandler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )

    logHandler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(logHandler)