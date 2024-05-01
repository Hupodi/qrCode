import webcolors
from typing import List, Tuple
from itertools import product

import png
import numpy as np


def plot_png(
    output_file: str,
    **kwargs,
) -> None:
    """
    Plot a QR code matrix in PNG format.
    """
    plot_matrix = color_wrapper(**kwargs)
    png.from_array(plot_matrix.tolist(), mode="RGB").save(output_file)


def color_wrapper(
    background_color: str = None,
    front_color: str = None,
    **kwargs,
) -> np.array:
    """
    Convert the given CSS color names to RGBs and pass along to draw_matrix.
    """
    colors = get_rgbs(background_color, front_color)
    return draw_matrix(
        **kwargs,
        **colors,
    )


def get_rgbs(background_color: str, front_color: str) -> dict:
    """
    Transform the given colors to RGB values.
    """
    if background_color is None:
        background_color = "white"
    if front_color is None:
        front_color = "black"

    return {
        "background_rgb": list(webcolors.name_to_rgb(background_color)),
        "front_rgb": list(webcolors.name_to_rgb(front_color)),
    }


def draw_matrix(
    matrix: np.array,
    background_rgb: List[int],
    front_rgb: List[int],
    bloc_size: int = 10,
) -> np.array:
    """
    Draw matrix:
        - Get background matrix
        - Fill with values
    Transform the given matrix to a matrix ready to be png-plotted.
    Use background and front color.
    Multiply each value to get pixels blocs of given bloc_size.
    """
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError(
            f"QR code should be a square matrix. Got size {matrix.shape[0]}, {matrix.shape[1]}."
        )
    if matrix.dtype != np.dtype("bool"):
        raise ValueError(
            f"QR code matrix should contain booleans. Got {matrix.dtype} instead."
        )

    background_matrix = get_background_matrix(
        n=matrix.shape[0],
        bloc_size=bloc_size,
        background_rgb=background_rgb,
    )
    return draw_values(
        working_matrix=background_matrix,
        value_matrix=matrix,
        front_rgb=front_rgb,
        bloc_size=bloc_size,
    )


def get_background_matrix(
    n: int,
    bloc_size: int,
    background_rgb: List[int],
) -> np.array:
    """
    Get a square matrix of the right size: (n * bloc_size, 3 x n * bloc_size), full of background_color.
    """
    size = n * bloc_size
    return np.array([background_rgb * size] * size)


def draw_values(
    working_matrix: np.array,
    value_matrix: np.array,
    front_rgb: List[int],
    bloc_size: int,
) -> np.array:
    """
    Draw each value from matrix to complete the resulting matrix.
    """
    iterator = np.nditer(value_matrix, flags=["multi_index"])
    for value in iterator:
        if not value:
            continue

        working_matrix = draw_bloc(
            working_matrix, iterator.multi_index, front_rgb, bloc_size
        )

    return working_matrix


def draw_bloc(
    working_matrix: np.array,
    indices: Tuple[int, int],
    front_rgb: List[int],
    bloc_size: int,
) -> np.array:
    """
    Draw a single bloc, by looping through each pixel of the bloc and filling the pixels with front_rgb triplets.
    """
    for i in product(
        range(bloc_size * indices[0], bloc_size * (indices[0] + 1)),
        range(bloc_size * indices[1], bloc_size * (indices[1] + 1)),
    ):
        working_matrix[i[0], (3 * i[1]) : (3 * i[1] + 3)] = front_rgb
    return working_matrix
