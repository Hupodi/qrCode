import numpy as np


def get_qr_matrix(bits: str, version: int) -> np.array:
    """
    From the encoded bits get the QR code boolean matrix
    """
    matrix = np.array()

    matrix = add_quiet_zone(matrix=matrix, quiet_zone_size=quiet_zone_size)


def add_quiet_zone(matrix: np.array, quiet_zone_size: int) -> np.array:
    """
    Add the quiet zone around the matrix.
    """
    result = np.zeros([size + 2 * quiet_zone_size for size in matrix.shape])
    result = np.array(result, dtype=bool)
    result[quiet_zone_size:-quiet_zone_size, quiet_zone_size:-quiet_zone_size] = matrix
    return result

