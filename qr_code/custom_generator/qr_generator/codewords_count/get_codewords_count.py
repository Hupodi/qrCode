from pathlib import Path

import pandas as pd

from qr_code.custom_generator.qr_generator.error_correction_level import (
    ErrorCorrectionLevel,
)

CODEWORDS_TABLE = pd.read_csv(Path(__file__).parent / "codewordsTable.csv")


def get_codewords_count(
    version: int, error_correction_level: ErrorCorrectionLevel
) -> int:
    """
    Get the total number of bytes to fill,
    corresponding to the given QR code version and error correction level
    """
    return CODEWORDS_TABLE.loc[
        (CODEWORDS_TABLE["Version"] == version)
        & (CODEWORDS_TABLE["EC Level"] == error_correction_level.name),
        "Codewords",
    ].squeeze()
