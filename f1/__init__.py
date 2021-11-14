import logging
import sys

from .settings import AppSettings

logging.getLogger().setLevel(logging.DEBUG)

try:
    from dotenv import load_dotenv
except ImportError:
    logging.error("Could not load required modules. Likely virtualenv not active or installed.")
    sys.exit(-1)

load_dotenv()

settings = AppSettings()
