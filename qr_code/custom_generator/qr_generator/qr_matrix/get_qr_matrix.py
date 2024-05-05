from typing import Tuple
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

from qr_code.custom_generator.plot_png import plot_png


ALIGNMENT_PATTERNS_TABLE = pd.read_csv(Path(__file__).parent / "AlignmentPatterns.csv")


def get_qr_matrix(bits: str, version: int, quiet_zone_size: int) -> np.array:
    """
    From the encoded bits get the QR code boolean matrix
    """
    size = get_matrix_size(version)
    matrix = np.full((size, size), False)
    written_matrix = np.full((size, size), False)

    matrix, written_matrix = add_finder_patterns(matrix, written_matrix)
    matrix, written_matrix = add_alignment_patterns(
        matrix=matrix, written_matrix=written_matrix, version=version
    )
    matrix, written_matrix = add_timing_patterns(
        matrix=matrix, written_matrix=written_matrix
    )
    matrix, written_matrix = add_dark_module(
        matrix=matrix, written_matrix=written_matrix
    )
    written_matrix = reserve_format_information(
        written_matrix
    )

    matrix = add_quiet_zone(matrix=matrix, quiet_zone_size=quiet_zone_size)
    # Debugging:
    plot_png(matrix=matrix, output_file="test_matrix.png")
    plot_png(matrix=written_matrix, output_file="test_written_matrix.png")

    return matrix


def get_matrix_size(version: int) -> int:
    """
    Get the matrix size depending on the version.
    """
    return 17 + 4 * version


def add_finder_patterns(matrix, written_matrix: np.array) -> Tuple[np.array, np.array]:
    """
    Add the three finder patterns to the matrix. Write them as written in the written_matrix
    """
    matrix, written_matrix = add_finder_pattern(
        matrix=matrix, written_matrix=written_matrix, top_left_indices=(0, 0)
    )
    matrix, written_matrix = add_finder_pattern(
        matrix=matrix,
        written_matrix=written_matrix,
        top_left_indices=(0, matrix.shape[0] - 7),
    )
    matrix, written_matrix = add_finder_pattern(
        matrix=matrix,
        written_matrix=written_matrix,
        top_left_indices=(matrix.shape[0] - 7, 0),
    )

    written_matrix = add_separators(written_matrix)

    return matrix, written_matrix


def add_finder_pattern(
    matrix: np.array, written_matrix: np.array, top_left_indices: Tuple[int, int]
) -> Tuple[np.array, np.array]:
    """
    Add a single finder pattern at the given location.
    """
    for offset in product(range(7), repeat=2):
        indices = tuple(
            [index + offset for index, offset in zip(offset, top_left_indices)]
        )
        written_matrix[indices] = True

        if offset[0] == 1 and 1 <= offset[1] <= 5:
            continue
        if offset[0] == 5 and 1 <= offset[1] <= 5:
            continue
        if offset[1] == 1 and 1 <= offset[0] <= 5:
            continue
        if offset[1] == 5 and 1 <= offset[0] <= 5:
            continue
        matrix[indices] = True

    return matrix, written_matrix


def add_separators(written_matrix: np.array) -> np.array:
    """
    Add the separator around finder patterns, stating them True in the written matrix.
    """
    offset = written_matrix.shape[0] - 8
    for index in range(8):
        written_matrix[7, index] = True
        written_matrix[7, index + offset] = True
        written_matrix[index, 7] = True
        written_matrix[index + offset, 7] = True
        written_matrix[offset, index] = True
        written_matrix[index, offset] = True
    return written_matrix


def add_alignment_patterns(
    matrix: np.array, written_matrix: np.array, version: int
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
            matrix=matrix, written_matrix=written_matrix, center_indices=center
        )

    return matrix, written_matrix


def add_alignment_pattern(
    matrix: np.array, written_matrix: np.array, center_indices: Tuple[int, int]
) -> Tuple[np.array, np.array]:
    """
    Add a single alignment pattern centered at center_indices, if it does not overlap with finder patterns
    """
    if (
        written_matrix[(center_indices[0] - 2, center_indices[1] - 2)] == True
        or written_matrix[(center_indices[0] - 2, center_indices[1] + 2)] == True
        or written_matrix[(center_indices[0] + 2, center_indices[1] - 2)] == True
        or written_matrix[(center_indices[0] + 2, center_indices[1] + 2)] == True
    ):
        return matrix, written_matrix

    for offset in product(range(-2, 3), repeat=2):
        indices = tuple(
            [index + offset for index, offset in zip(offset, center_indices)]
        )
        written_matrix[indices] = True

        if offset[0] == -1 and -1 <= offset[1] <= 1:
            continue
        if offset[0] == 1 and -1 <= offset[1] <= 1:
            continue
        if offset[1] == -1 and -1 <= offset[0] <= 1:
            continue
        if offset[1] == 1 and -1 <= offset[0] <= 1:
            continue
        matrix[indices] = True

    return matrix, written_matrix


def add_timing_patterns(matrix: np.array, written_matrix: np.array) -> Tuple[np.array, np.array]:
    """
    Add timing patterns: row 6 and col 6. No need to worry about alignment patterns, they always coincide.
    """
    alternating_value = True  # Start with a black square
    for index in range(6, matrix.shape[0] - 7):
        matrix[6, index] = alternating_value
        matrix[index, 6] = alternating_value
        written_matrix[index, 6] = True
        written_matrix[6, index] = True
        alternating_value = not alternating_value

    return matrix, written_matrix


def add_dark_module(matrix: np.array, written_matrix: np.array) -> Tuple[np.array, np.array]:
    """
    Add a single dark cell next to the bottom right finder pattern.
    """
    position = matrix.shape[0] - 8
    matrix[position, 8] = True
    written_matrix[position, 8] = True
    return matrix, written_matrix


def reserve_format_information(written_matrix: np.array) -> np.array:
    """
    Reserve the spots for format information.
    """
    size = written_matrix.shape[0]
    for index in range(9):
        written_matrix[index, 8] = True
        written_matrix[8, index] = True
    for index in range(1, 9):
        written_matrix[size - index, 8] = True
        written_matrix[8, size - index] = True

    return written_matrix


def add_quiet_zone(matrix: np.array, quiet_zone_size: int) -> np.array:
    """
    Add the quiet zone around the matrix.
    """
    result = np.zeros([size + 2 * quiet_zone_size for size in matrix.shape])
    result = np.array(result, dtype=bool)
    result[quiet_zone_size:-quiet_zone_size, quiet_zone_size:-quiet_zone_size] = matrix
    return result
