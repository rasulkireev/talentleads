import logging
import math

logger = logging.getLogger(__file__)


def floor_to_thousands(x):
    return int(math.floor(x / 1000.0)) * 1000


def floor_to_tens(x):
    return int(math.floor(x / 10.0)) * 10
