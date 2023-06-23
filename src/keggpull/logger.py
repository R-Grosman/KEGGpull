import logging
import sys

__author__ = "R-Grosman"
__copyright__ = "R-Grosman"
__license__ = "MIT"
__version__ = "0.2.0"


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))