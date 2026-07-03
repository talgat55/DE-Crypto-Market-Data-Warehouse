import logging

from config import LOG_DATE_FORMAT, LOG_FORMAT, LOG_LEVEL


def get_logger(name: str):
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )

    return logging.getLogger(name)