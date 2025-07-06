import logging
from fastapi.logger import logger as fastapi_logger

log_fmt = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = fastapi_logger
