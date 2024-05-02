from enum import Enum


class ErrorCorrectionLevel(Enum):
    """
    Enum for the four level of error correction.
    """

    L = 0.07
    M = 0.15
    Q = 0.25
    H = 0.3
