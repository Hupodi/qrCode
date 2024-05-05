from typing import List
from pathlib import Path
import json

import pandas as pd


LOG_TABLE = pd.read_csv(Path(__file__).parent / "LogTable.csv")


def get_all_generator_polynomials(n: int = 68):
    """
    Generate all generator polynomials from 1 to n.
    Polynomial are formatted as the list of exponent of 2, from n to 0.
    """
    result = {1: [0, 0]}
    for degree in range(2, n + 1):
        result[degree] = get_next_polynomial(result[degree - 1])

    with open(
        "qr_code/custom_generator/qr_generator/error_correction/generatorPolynomial.json",
        "w",
    ) as f:
        json.dump(result, f)


def get_next_polynomial(polynomial: List[int]) -> List[int]:
    """
    Given a generator polynomial, get the next one (increasing one degree).
    """
    n = len(polynomial) - 1
    multiplicator = [0, n]
    result = [0] * (n + 2)

    for index_1, exponent_1 in enumerate(polynomial):
        for index_2, exponent_2 in enumerate(multiplicator):
            degree_1 = len(polynomial) - index_1 - 1
            degree_2 = len(multiplicator) - index_2 - 1
            degree = degree_1 + degree_2
            index = len(result) - (degree + 1)
            exponent = exponent_1 + exponent_2
            if exponent > 255:
                exponent = exponent % 255

            if result[index] == 0:
                result[index] = exponent
            else:
                result[index] = get_exponent(get_int(result[index]) ^ get_int(exponent))

    return result


def get_int(exponent: int) -> int:
    """
    From exponent get int
    """
    return LOG_TABLE.loc[LOG_TABLE["Exponent"] == exponent, "Integer"].squeeze()


def get_exponent(int_value: int) -> int:
    """
    From int get exponent
    """
    if int_value == 0:
        return 0

    return int(
        LOG_TABLE.loc[LOG_TABLE["Integer"] == int_value, "Exponent"].iloc[0].squeeze()
    )
