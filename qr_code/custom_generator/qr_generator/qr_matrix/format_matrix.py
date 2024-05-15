from pathlib import Path

import numpy as np
import pandas as pd

from qr_code.custom_generator.qr_generator.error_correction_level import ErrorCorrectionLevel


def format_matrix(error_correction_level: ErrorCorrectionLevel, matrix: np.array, mask_number: int) -> np.array:
    """
    Final formatting of the matrix: Add format and version information
    """
    format_info_table = pd.read_csv(Path(__file__).parent / "FormatInformation.csv")

    format_info_bits = format_info_table.loc[
        (format_info_table["ECC Level"] == error_correction_level.name) & (format_info_table["Mask Pattern"] == mask_number), "Type Information Bits"
    ].squeeze()

    matrix = fill_format_info(matrix=matrix, format_info_bits=str(format_info_bits))
    matrix = add_version_information(matrix=matrix)

    return matrix

def fill_format_info(matrix: np.array, format_info_bits: str) -> np.array:
    """
    Fill in the matrix the format_info_bits
    """
    n = matrix.shape[0]

    for i, bit in enumerate(format_info_bits):

        # Top left corner:
        if i <= 5:
            matrix[8, i] = (bit == "1")
        elif i <= 6:
            matrix[8, i + 1] = (bit == "1")
        elif i == 8:
            matrix[7, 8] = (bit == "1")
        else:
            matrix[14 - i, 8] = (bit == "1")

        # Bottom left and top right:
        if i <= 6:
            matrix[n - 1 - i, 8] = (bit == "1")
        else:
            matrix[8, n - 15 + i] = (bit == "1")

    return matrix


def add_version_information(matrix: np.array) -> np.array:
    """
    Add the version information part for version >= 7
    """
    n = matrix.shape[0]
    version = int(n - 17 / 4)
    if version < 7:
        return matrix

    version_information_table = pd.read_csv(Path(__file__).parent / "VersionInformation.csv")
    version_information_bits = version_information_table.loc[
        version_information_table["Version"] == version, "Version Information String"
    ].squeeze()
    version_information_bits = str(version_information_bits)

    # Bottom left:
    index = 0
    for j in range(6):
        for i in range(3):
            matrix[n - 11 + i, j] = version_information_bits[index]
    # Top right:
    index = 0
    for i in range(6):
        for j in range(3):
            matrix[i, n - 11 + j] = version_information_bits[index]

    return matrix
