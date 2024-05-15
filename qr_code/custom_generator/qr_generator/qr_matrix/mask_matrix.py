import numpy as np


def mask_matrix(matrix: np.array, protected_matrix: np.array) -> np.array:
    """
    Apply data masking: Evaluate each of the 8 masking patterns according to the 4 criterion, apply the correct one.
    """
    return