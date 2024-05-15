from typing import Tuple
from itertools import product

import numpy as np
import pandas as pd

from qr_code.custom_generator.plot_png import plot_png


ALIGNMENT_PATTERNS_TABLE = pd.read_csv("qr_code/custom_generator/qr_generator/qr_matrix/AlignmentPatterns.csv")


def get_qr_matrix(bits: str, version: int) -> Tuple[np.array, np.array]:
    """
    From the encoded bits get the QR code boolean matrix
    """
    size = get_matrix_size(version)
    matrix = np.full((size, size), False)
    protected_matrix = np.full((size, size), False)

    matrix, protected_matrix = add_finder_patterns(matrix, protected_matrix)
    matrix, protected_matrix = add_alignment_patterns(
        matrix=matrix, protected_matrix=protected_matrix, version=version
    )
    matrix, protected_matrix = add_timing_patterns(
        matrix=matrix, protected_matrix=protected_matrix
    )
    matrix, protected_matrix = add_dark_module(
        matrix=matrix, protected_matrix=protected_matrix
    )
    protected_matrix = reserve_format_information(
        protected_matrix
    )
    protected_matrix = reserve_version_information(
        version=version, protected_matrix=protected_matrix
    )

    matrix, protected_matrix = place_bits(
        matrix=matrix, protected_matrix=protected_matrix, bits=bits
    )

    # Debugging:
    plot_png(matrix=matrix, output_file="test_matrix.png")
    plot_png(matrix=protected_matrix, output_file="test_protected_matrix_matrix.png")

    return matrix, protected_matrix


def get_matrix_size(version: int) -> int:
    """
    Get the matrix size depending on the version.
    """
    return 17 + 4 * version


def add_finder_patterns(matrix, protected_matrix: np.array) -> Tuple[np.array, np.array]:
    """
    Add the three finder patterns to the matrix. Write them as protected in the protected_matrix
    """
    matrix, protected_matrix = add_finder_pattern(
        matrix=matrix, protected_matrix=protected_matrix, top_left_indices=(0, 0)
    )
    matrix, protected_matrix = add_finder_pattern(
        matrix=matrix,
        protected_matrix=protected_matrix,
        top_left_indices=(0, matrix.shape[0] - 7),
    )
    matrix, protected_matrix = add_finder_pattern(
        matrix=matrix,
        protected_matrix=protected_matrix,
        top_left_indices=(matrix.shape[0] - 7, 0),
    )

    protected_matrix = add_separators(protected_matrix)

    return matrix, protected_matrix


def add_finder_pattern(
    matrix: np.array, protected_matrix: np.array, top_left_indices: Tuple[int, int]
) -> Tuple[np.array, np.array]:
    """
    Add a single finder pattern at the given location.
    """
    for offset in product(range(7), repeat=2):
        indices = tuple(
            [index + offset for index, offset in zip(offset, top_left_indices)]
        )
        protected_matrix[indices] = True

        if offset[0] == 1 and 1 <= offset[1] <= 5:
            continue
        if offset[0] == 5 and 1 <= offset[1] <= 5:
            continue
        if offset[1] == 1 and 1 <= offset[0] <= 5:
            continue
        if offset[1] == 5 and 1 <= offset[0] <= 5:
            continue
        matrix[indices] = True

    return matrix, protected_matrix


def add_separators(protected_matrix: np.array) -> np.array:
    """
    Add the separator around finder patterns, stating them True in the protected matrix.
    """
    offset = protected_matrix.shape[0] - 8
    for index in range(8):
        protected_matrix[7, index] = True
        protected_matrix[7, index + offset] = True
        protected_matrix[index, 7] = True
        protected_matrix[index + offset, 7] = True
        protected_matrix[offset, index] = True
        protected_matrix[index, offset] = True
    return protected_matrix


def add_alignment_patterns(
    matrix: np.array, protected_matrix: np.array, version: int
) -> Tuple[np.array, np.array]:
    """
    Add alignment patterns.
    """
    centers = (
        ALIGNMENT_PATTERNS_TABLE.loc[ALIGNMENT_PATTERNS_TABLE["Version"] == version]
        .squeeze()
        .to_list()
    )
    centers = centers[1:]
    centers = [int(center) for center in centers if not pd.isna(center)]

    for center in product(centers, repeat=2):
        add_alignment_pattern(
            matrix=matrix, protected_matrix=protected_matrix, center_indices=center
        )

    return matrix, protected_matrix


def add_alignment_pattern(
    matrix: np.array, protected_matrix: np.array, center_indices: Tuple[int, int]
) -> Tuple[np.array, np.array]:
    """
    Add a single alignment pattern centered at center_indices, if it does not overlap with finder patterns
    """
    if (
        protected_matrix[(center_indices[0] - 2, center_indices[1] - 2)] == True
        or protected_matrix[(center_indices[0] - 2, center_indices[1] + 2)] == True
        or protected_matrix[(center_indices[0] + 2, center_indices[1] - 2)] == True
        or protected_matrix[(center_indices[0] + 2, center_indices[1] + 2)] == True
    ):
        return matrix, protected_matrix

    for offset in product(range(-2, 3), repeat=2):
        indices = tuple(
            [index + offset for index, offset in zip(offset, center_indices)]
        )
        protected_matrix[indices] = True

        if offset[0] == -1 and -1 <= offset[1] <= 1:
            continue
        if offset[0] == 1 and -1 <= offset[1] <= 1:
            continue
        if offset[1] == -1 and -1 <= offset[0] <= 1:
            continue
        if offset[1] == 1 and -1 <= offset[0] <= 1:
            continue
        matrix[indices] = True

    return matrix, protected_matrix


def add_timing_patterns(matrix: np.array, protected_matrix: np.array) -> Tuple[np.array, np.array]:
    """
    Add timing patterns: row 6 and col 6. No need to worry about alignment patterns, they always coincide.
    """
    alternating_value = True  # Start with a black square
    for index in range(6, matrix.shape[0] - 7):
        matrix[6, index] = alternating_value
        matrix[index, 6] = alternating_value
        protected_matrix[index, 6] = True
        protected_matrix[6, index] = True
        alternating_value = not alternating_value

    return matrix, protected_matrix


def add_dark_module(matrix: np.array, protected_matrix: np.array) -> Tuple[np.array, np.array]:
    """
    Add a single dark cell next to the bottom right finder pattern.
    """
    position = matrix.shape[0] - 8
    matrix[position, 8] = True
    protected_matrix[position, 8] = True
    return matrix, protected_matrix


def reserve_format_information(protected_matrix: np.array) -> np.array:
    """
    Reserve the spots for format information.
    """
    size = protected_matrix.shape[0]
    for index in range(9):
        protected_matrix[index, 8] = True
        protected_matrix[8, index] = True
    for index in range(1, 9):
        protected_matrix[size - index, 8] = True
        protected_matrix[8, size - index] = True

    return protected_matrix


def reserve_version_information(version: int, protected_matrix: np.array) -> np.array:
    """
    Reserve cells for version information.
    """
    size = protected_matrix.shape[0]
    if version < 7:
        return protected_matrix

    for i in range(3):
        for j in range(6):
            protected_matrix[j, size - 11 + i] = True
            protected_matrix[size - 11 + i, j] = True

    return protected_matrix


def place_bits(matrix: np.array, protected_matrix: np.array, bits: str) -> Tuple[np.array, np.array]:
    """
    Place data bits in the matrix.
    """
    if len(bits) != (matrix.shape[0] ** 2 - protected_matrix.sum()):
        raise ValueError(f"Encoded message Bits size {len(bits)} is different than the available slots in the matrix ({(matrix.shape[0] ** 2 - protected_matrix.sum())}).")
    row_direction = -1
    row = matrix.shape[0] - 1
    column = matrix.shape[0] - 1
    column_offset = False

    for i, bit in enumerate(bits):

        while protected_matrix[row, column - column_offset] == True:
            row_direction, row, column, column_offset = move_cursor(row_direction, row, column, column_offset, matrix.shape[0])

        matrix[row, column - column_offset] = (bit == "1")
        protected_matrix[row, column - column_offset] = True

    return matrix, protected_matrix


def move_cursor(row_direction: int, row: int, column: int, column_offset: bool, size: int) -> Tuple[int, int, int, bool]:
    """
    Move the filling bits cursor, respecting the logic.
    """
    if column_offset is False:
        return row_direction, row, column, True
    if 0 <= (row + row_direction) < size:
        return row_direction, row + row_direction, column, False
    if column - 2 == 6:
        return - row_direction, row, column - 3, False
    return - row_direction, row, column - 2, False
