import numpy as np

from qr_code.custom_generator.qr_generator.error_correction_level import ErrorCorrectionLevel


def format_matrix(error_correction_level: ErrorCorrectionLevel, matrix: np.array, protected_matrix: np.array, mask_string: str) -> np.array:
    """
    Final formatting of the matrix: Add format and version information
    """
    version_str = {
        ErrorCorrectionLevel.L: "01",
        ErrorCorrectionLevel.M: "00",
        ErrorCorrectionLevel.Q: "11",
        ErrorCorrectionLevel.H: "10",
    }[error_correction_level]
    format_string = version_str + mask_string

