from typing import List

from .generator_polynomials import get_int, get_exponent


def divide_polynomials(quotien: List[int], divisor: List[int]) -> List[int]:
    """
    Polynomial division
    """
    steps = len(quotien)
    running_quotien = quotien

    for step in range(steps):

        multiplication_exponent = running_quotien[0]
        multiplied_polynomial = [(exponent + multiplication_exponent) % 255 for exponent in divisor]

        # XOR
        result = []
        for index, quotien_exponent in enumerate(running_quotien):

            if index == 0:
                if get_int(quotien_exponent) ^ get_int(multiplied_polynomial[index]) != 0:
                    raise ValueError
                continue

            divisor_int = get_int(multiplied_polynomial[index]) if index < len(multiplied_polynomial) else 0
            result.append(get_int(quotien_exponent) ^ divisor_int)

        if len(running_quotien) < len(divisor):
            divisor_int = get_int(multiplied_polynomial[index + 1]) if (index + 1) < len(multiplied_polynomial) else 0
            result.append(divisor_int)

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
