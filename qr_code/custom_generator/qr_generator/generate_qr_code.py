import numpy as np

from qr_code.custom_generator.qr_generator.error_correction_level import ErrorCorrectionLevel
from qr_code.custom_generator.qr_generator.level import get_level


def generate_qr_code(
    url: str,
    error_correction_level: ErrorCorrectionLevel = ErrorCorrectionLevel.H,
    quiet_zone_size: int = 4,
) -> np.array:
    """
    Generate a QR code matrix corresponding to the given url.
    """
    level = get_level(message_size=len(url), error_correction_level=error_correction_level)

    # Dummy output for now
    result = np.array()
    add_quiet_zone(matrix=result, quiet_zone_size=quiet_zone_size)
    return np.array


def add_quiet_zone(matrix: np.array, quiet_zone_size: int) -> np.array:
    """
    Add the quiet zone around the matrix.
    """
    result = np.zeros([size + 2 * quiet_zone_size for size in matrix.shape])
    result = np.array(result, dtype=bool)
    result[quiet_zone_size:-quiet_zone_size, quiet_zone_size:-quiet_zone_size] = matrix
    return result
