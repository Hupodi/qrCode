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
    """
    config = CODEWORDS_TABLE.loc[
        (CODEWORDS_TABLE["Version"] == version)
        & (CODEWORDS_TABLE["EC Level"] == error_correction_level.name)
    ].squeeze()
    group_1 = []
    group_2 = []
    for byte_index in range(len(bits) // 8):
        codeword = bits[(8 * byte_index):(8 * (byte_index + 1))]

        if (len(group_1) < config["Group 1 Blocks"]) or (len(group_1) == config["Group 1 Blocks"] and len(group_1[-1]) < config["Group 1 Codewords Per Block"]):
            if len(group_1[-1]) < config["Group 1 Codewords Per Block"]:
                group_1[-1].append(codeword)
            else:
                group_1.append([codeword])
        else:
            if len(group_2[-1]) < config["Group 2 Codewords Per Block"]:
                group_2[-1].append(codeword)
            else:
                group_2.append([codeword])

    return group_1, group_2
