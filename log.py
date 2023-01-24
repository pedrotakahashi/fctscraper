import os
import sys
import logging

logger = logging.getLogger(__name__)


def log_file():
    home = os.path.expanduser("~")
    logs_dir = os.path.join(home, "media_downloader")
    logs_path = os.path.join(logs_dir, "log.txt")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    return logs_path


FILE_HANDLER = logging.FileHandler(log_file())
FILE_HANDLER.setFormatter(
    logging.Formatter("%(asctime)s.%(msecs)03d - %(message)s", "%d/%m/%Y %H:%M:%S")
)
FILE_HANDLER.setLevel(logging.DEBUG)
logger.addHandler(FILE_HANDLER)


STDOUT_HANDLER = logging.StreamHandler(stream=sys.stdout)
STDOUT_HANDLER.setLevel(logging.DEBUG)
logger.addHandler(STDOUT_HANDLER)
logger.setLevel(logging.DEBUG)
