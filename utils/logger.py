import loguru
import datetime

from models.requests import GeneratePricesRequest


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
        rotation="1 day",
        retention="1 day",
        level="INFO",
    )
    return logger


def log_request(logger: loguru.logger, request: GeneratePricesRequest) -> None:
    """
    Log the requests contents to the log file for a given logger.

    :param logger: loguru logger
    :param request: request containing the date, country code, granularity, and commodity
    :return: None
    """
    logger.info(f"for_date: {request.for_date}")
    logger.info(f"country_code: {request.country_code}")
    logger.info(f"granularity: {request.granularity}")
    logger.info(f"commodity: {request.commodity}")
    return None
