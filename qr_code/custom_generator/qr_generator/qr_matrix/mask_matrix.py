import copy
from itertools import product
import math

import numpy as np


mask_formulas = [
    lambda i, j: (i + j) % 2 == 0,
    lambda i, j: i % 2 == 0,
    lambda i, j: j % 3 == 0,
    lambda i, j: (i + j) % 3 == 0,
    lambda i, j: (math.floor(i / 2) + math.floor(j) / 3) % 2 == 0,
    lambda i, j: (i * j) % 2 + (i * j) % 3 == 0,
    lambda i, j: ((i * j) % 2 + (i * j) % 3) % 2 == 0,
    lambda i, j: ((i + j) % 2 + (i * j) % 3) % 2 == 0,
]

mask_methods = [
    lambda matrix, protected_matrix: mask(matrix=matrix, protected_matrix=protected_matrix, formula=formula) for formula in mask_formulas
]


def mask_matrix(matrix: np.array, protected_matrix: np.array) -> np.array:
    """
    Apply data masking: Evaluate each of the 8 masking patterns according to the 4 criterion, apply the correct one.
    """
    min_penalty = np.inf
    selected_mask = None
    for mask_method in mask_methods:
        penalty = get_penalty_score(mask_method(matrix=matrix, protected_matrix=protected_matrix))
        if penalty < min_penalty:
            min_penalty = penalty
            selected_mask = mask_method

    return selected_mask(matrix=matrix, protected_matrix=protected_matrix)


def get_penalty_score(matrix: np.array) -> int:
    """
    Evaluate the matrix according to all 4 evaluation criterion, and returning the sum.
    """
    penalty = 0
    for method in [evaluate_by_row_and_column, evaluate_by_2_x_2_blocks, evaluate_by_finder_pattern, evaluate_by_ratio]:
        penalty += method(matrix)

    return penalty


def evaluate_by_row_and_column(matrix: np.array) -> int:
    """
    Evaluate the given matrix by adding 3 to the penalty each time 5 consecutive bits are similar,
    and 1 more for each additional consecutive (7 in a row gives 3 + 2 = 5)
    """
    penalty = 0
    for row in matrix:
        penalty += array_penalty(row)

    for column in matrix.T:
        penalty += array_penalty(column)
    return penalty


def array_penalty(array: np.array) -> int:
    """
    Compute the penalty over one row or one column
    """
    penalty = 0
    streak = []
    for value in array:
        if len(streak) > 0 and value == streak[-1]:
            streak.append(value)
        else:
            if len(streak) >= 5:
                penalty += 3 + (len(streak) - 5)
            streak = [value]
    return penalty


def evaluate_by_2_x_2_blocks(matrix: np.array) -> int:
    """
    Evaluate by adding 3 to the penalty for each 2x2 block of similar bits.
    """
    penalty = 0
    for indices in product(range(matrix.shape[0] - 1), repeat=2):
        if matrix[indices] == matrix[indices[0], indices[1] + 1] == matrix[indices[0] + 1, indices[1]] == matrix[indices[0] + 1, indices[1] + 1]:
            penalty += 3

    return penalty


def evaluate_by_finder_pattern(matrix: np.array) -> int:
    """
    Evaluate by adding 40 each time a specific pattern (a-like the finder patterns) is found.
    """
    penalty = 0
    for row in matrix:
        penalty += finder_pattern_penalty(row)

    for column in matrix.T:
        penalty += finder_pattern_penalty(column)
    return penalty


def finder_pattern_penalty(array: np.array) -> int:
    """
    Look for the specific patterns in the row / col and add 40.
    """
    penalty = 0
    for i in range(len(array) - 11):
        if np.array_equal(array[i:(i+11)], [True, False, True, True, True, False, True, False, False, False, False]) or np.array_equal(array[i:(i+11)], [False, False, False, False, True, False, True, True, True, False, True]):
            penalty += 40

    return penalty


def evaluate_by_ratio(matrix: np.array) -> int:
    """
    Evaluate by estimating the black-white ratio of the matrix.
    """
    ratio = (matrix.sum() / matrix.shape[0] ** 2) * 100
    small = abs(ratio // 5 * 5 - 50) / 5
    high = abs((ratio // 5 + 1) * 5 - 50) / 5

    return min(small, high) * 10


def mask(matrix: np.array, protected_matrix: np.array, formula: callable) -> np.array:
    """
    Mask the matrix using the given formula
    """
    masked_matrix = copy.deepcopy(matrix)
    for indices in product(range(matrix.shape[0]), repeat=2):
        if protected_matrix[indices] is False and formula(indices[0], indices[1]):
            masked_matrix[indices] = not masked_matrix[indices]
    return masked_matrix

