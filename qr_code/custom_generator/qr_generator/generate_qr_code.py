import numpy as np


def generate_qr_code(url: str) -> np.array:
    """
    Generate a QR code matrix corresponding to the given url.
    """
    return np.array


def add_quiet_zone(matrix: np.array, quiet_zone_size: int) -> np.array:
    """
    Add the quiet zone around the matrix.
    """
    result = np.zeros([size + 2 * quiet_zone_size for size in matrix.shape])
    result = np.array(result, dtype=bool)
    result[quiet_zone_size:-quiet_zone_size,quiet_zone_size:-quiet_zone_size] = matrix
    return result
