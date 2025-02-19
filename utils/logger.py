import loguru
import datetime


def get_logger(logger_name: str) -> loguru.logger:
    """
    Return a logger with the specified name.

    :param logger_name: name of the logger
    :return: loguru.logger
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    logger = loguru.logger
    logger.add(
        f"logs/{logger_name}-{today}.log",
        rotation="1 hour",
        retention="1 hour",
        level="INFO",
        mode="w",
    )
    return logger
