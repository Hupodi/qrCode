from typing import List

from .generator_polynomials import get_int, get_exponent


def divide_polynomials(quotien: List[int], divisor: List[int]) -> List[int]:
    """
    Polynomial division, where quotien and division are Lists of integers {0, 255}.
    Divisor should be exponents of 2.
    """
    steps = len(quotien)
    running_quotien = [get_exponent(int_value) for int_value in quotien]

    for step in range(steps):
        multiplication_exponent = running_quotien[0]
        multiplied_polynomial = [
            (exponent + multiplication_exponent) % 255 for exponent in divisor
        ]

        # XOR
        result = []
        for index in range(max(len(running_quotien), len(multiplied_polynomial))):
            quotien_int = (
                get_int(running_quotien[index]) if index < len(running_quotien) else 0
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

        running_quotien = [get_exponent(int_value) for int_value in result]
    return result


def modulo_if_too_high(exponent: int) -> int:
    """
    Return exponent % 255 if exponent > 255
    """
    if exponent > 255:
        return exponent % 255
    else:
        return exponent
