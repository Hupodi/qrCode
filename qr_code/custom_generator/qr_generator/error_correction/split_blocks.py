from typing import Tuple

from qr_code.custom_generator.qr_generator.error_correction_level import (
    ErrorCorrectionLevel,
)
from qr_code.custom_generator.qr_generator.codewords_count import CODEWORDS_TABLE


def split_blocks(
    bits: str, version: int, error_correction_level: ErrorCorrectionLevel
) -> Tuple[list, list]:
    """
    Split bits into blocks according to the codewords table.
    Also, convert str binary codewords to the corresponding integer in {0, 255}.
    """
    config = CODEWORDS_TABLE.loc[
        (CODEWORDS_TABLE["Version"] == version)
        & (CODEWORDS_TABLE["EC Level"] == error_correction_level.name)
    ].squeeze()
    group_1 = []
    group_2 = []
    for byte_index in range(len(bits) // 8):
        codeword_int = bits_str_to_int(bits[(8 * byte_index) : (8 * (byte_index + 1))])

        if (len(group_1) < config["Group 1 Blocks"]) or (
            len(group_1) == config["Group 1 Blocks"]
            and len(group_1[-1]) < config["Group 1 Codewords Per Block"]
        ):
            if len(group_1[-1]) < config["Group 1 Codewords Per Block"]:
                group_1[-1].append(codeword_int)
            else:
                group_1.append([codeword_int])
        else:
            if len(group_2[-1]) < config["Group 2 Codewords Per Block"]:
                group_2[-1].append(codeword_int)
            else:
                group_2.append([codeword_int])

    return group_1, group_2


def bits_str_to_int(codeword: str) -> int:
    """
    Transform a bit codeword into the 0~255 corresponding int.
    """
    return int(codeword, 2)
