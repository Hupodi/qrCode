import json

import pandas as pd

from qr_code.custom_generator.qr_generator.error_correction_level import ErrorCorrectionLevel
from qr_code.custom_generator.qr_generator.codewords_count import CODEWORDS_TABLE
from qr_code.custom_generator.qr_generator.error_correction.split_blocks import split_blocks
from qr_code.custom_generator.qr_generator.error_correction.polynomial_division import get_int, get_exponent, divide_polynomials


with open("qr_code/custom_generator/qr_generator/error_correction/generatorPolynomial.json", "r") as f:
    GENERATOR_POLYNOMIALS = json.load(f)

REMAINDER_BITS = pd.read_csv("qr_code/custom_generator/qr_generator/error_correction/remainderBits.csv")


def encode_message(raw_data_bits: str, version: int, error_correction_level: ErrorCorrectionLevel) -> str:
    """
    Encode the message
    """
    group_1, group_2 = split_blocks(bits=raw_data_bits, version=version, error_correction_level=error_correction_level)

    error_correction_codewords_per_block = CODEWORDS_TABLE.loc[
        (CODEWORDS_TABLE["Version"] == version)
        & (CODEWORDS_TABLE["EC Level"] == error_correction_level.name),
        "EC Codewords Per Block",
    ].squeeze()
    generator_polynomial = GENERATOR_POLYNOMIALS[str(error_correction_codewords_per_block)]

    error_correction_codewords = []
    for block_ints in group_1 + group_2:
        error_correction_codewords.append(divide_polynomials(block_ints, generator_polynomial))

    # Interleaving data
    data_interleaved = []
    for index in range(max(len(block) for block in group_1 + group_2)):
        for block in group_1 + group_2:
            if index < len(block):
                data_interleaved.append(block[index])

    for index in range(len(error_correction_codewords[0])):
        for block in error_correction_codewords:
            data_interleaved.append(block[index])

    data_interleaved_bits = "".join(['{0:08b}'.format(int_value) for int_value in data_interleaved])
    return add_remainder_bits(data_interleaved_bits, version)


def add_remainder_bits(bits: str, version: int) -> str:
    """
    Add the remainder bits depending on the QR code version.
    """
    amount = REMAINDER_BITS.loc[REMAINDER_BITS["Version"] == version, "Remainder Bits"].squeeze()
    return bits + "0" * amount
