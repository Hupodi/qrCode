import numpy as np

from qr_code.custom_generator.qr_generator.error_correction_level import (
    ErrorCorrectionLevel,
)
from qr_code.custom_generator.qr_generator.version import get_version
from qr_code.custom_generator.qr_generator.character_count import (
    get_character_count_indicator,
)
from qr_code.custom_generator.qr_generator.encode_data import encode_data
from qr_code.custom_generator.qr_generator.codewords_count import get_codewords_count
from qr_code.custom_generator.qr_generator.error_correction import encode_message
from qr_code.custom_generator.qr_generator.qr_matrix import get_qr_matrix


def generate_qr_code(
    url: str,
    error_correction_level: ErrorCorrectionLevel = ErrorCorrectionLevel.H,
    quiet_zone_size: int = 4,
    mode: str = "Byte",
) -> np.array:
    """
    Generate a QR code matrix corresponding to the given url.
    """
    if mode != "Byte":
        raise ValueError(
            "Only Byte mode is supported. Structure is there to implement the others, though."
        )

    version = get_version(
        message_size=len(url), error_correction_level=error_correction_level, mode=mode
    )
    raw_data_bits = get_mode_indicator(mode)
    raw_data_bits += get_character_count_indicator(url=url, version=version, mode=mode)
    raw_data_bits += encode_data(url=url, mode=mode)

    codewords_count = get_codewords_count(
        version=version, error_correction_level=error_correction_level
    )
    raw_data_bits += get_terminator(
        size=len(raw_data_bits), codewords_count=codewords_count
    )
    raw_data_bits = ensure_multiple_of_eight(raw_data_bits)
    raw_data_bits = fill_to_max_size(
        bits=raw_data_bits, codewords_count=codewords_count
    )

    corrected_bits = encode_message(raw_data_bits=raw_data_bits, version=version, error_correction_level=error_correction_level)
    matrix = get_qr_matrix(
        bits=corrected_bits, version=version, quiet_zone_size=quiet_zone_size
    )

    return matrix


def get_mode_indicator(mode: str) -> str:
    """
    Get mode indicator 4-bits.
    """
    mode_to_indicator = {
        "Numeric": "0001",
        "Alphanumeric": "0010",
        "Byte": "0100",
        "Kanji": "1000",
        "ECI": "0111",
    }
    return mode_to_indicator[mode]


def get_terminator(size: int, codewords_count: int) -> str:
    """
    Get the terminator string, up to 4 zeros.
    """
    return "0" * min(4, codewords_count * 8 - size)


def ensure_multiple_of_eight(bits: str) -> str:
    """
    Ensure the data bits length is a multiple of 8, by adding 0s at the end.
    """
    remainder = len(bits) % 8
    return bits + "0" * remainder


def fill_to_max_size(bits: str, codewords_count: int) -> str:
    """
    Final step of raw bits padding, add 11101100 00010001 bytes until 8 * codewords_count is reached.
    """
    bytes_to_add = codewords_count - (len(bits) // 8)
    return (
        bits
        + "1110110000010001" * (bytes_to_add // 2)
        + "11101100" * (bytes_to_add % 2)
    )
