from typing import List

from .generator_polynomials import get_int, get_exponent


def divide_polynomials(quotien: List[int], divisor: List[int]) -> List[int]:
    """
    Polynomial division, where quotien and division are Lists of integers {0, 255}.
    Divisor should be exponents of 2.
    """
    steps = len(quotien)
    # running_quotien = [get_exponent(int_value) for int_value in quotien]
    running_quotien_ints = quotien

    for step in range(steps):
        multiplication_exponent = get_exponent(running_quotien_ints[0])
        multiplied_polynomial = [
            (exponent + multiplication_exponent) % 255 for exponent in divisor
        ]

        # XOR
        result = []
        for index in range(max(len(running_quotien_ints), len(multiplied_polynomial))):
            quotien_int = (
                running_quotien_ints[index] if index < len(running_quotien_ints) else 0
            )
            divisor_int = (
                get_int(multiplied_polynomial[index])
                if index < len(multiplied_polynomial)
                else 0
            )

            if index == 0:
                if quotien_int ^ divisor_int != 0:
                    raise ValueError
                continue

            result.append(quotien_int ^ divisor_int)

        running_quotien_ints = result
    return result


def modulo_if_too_high(exponent: int) -> int:
    """
    Return exponent % 255 if exponent > 255
    """
    if exponent > 255:
        return exponent % 255
    else:
        return exponent
