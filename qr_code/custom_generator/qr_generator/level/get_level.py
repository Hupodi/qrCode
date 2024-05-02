import logging
from pathlib import Path

import pandas as pd

from qr_code.custom_generator.qr_generator.error_correction_level import (
    ErrorCorrectionLevel,
)


def get_level(
    message_size: int, error_correction_level: ErrorCorrectionLevel, mode: str = "Byte"
) -> int:
    """
    From message size, determine the QR code level to use, in {1, 40}.
    """
    table = pd.read_csv(Path(__file__).parent / "capacityTable.csv")

    try:
        return min(
            table.loc[
                (table["Error Correction Level"] == error_correction_level.name)
                & (table[mode] >= message_size),
                "Version",
            ]
        )
    except ValueError as err:
        logging.error(err)
        raise ValueError(
            f"message size {message_size} is too long to be supported with mode {mode} "
            f"and error correction level {error_correction_level.name}."
        )
