from pathlib import Path

import pandas as pd

from qr_code.custom_generator.qr_generator.error_correction_level import ErrorCorrectionLevel


def get_codewords_count(version: int, error_correction_level: ErrorCorrectionLevel) -> int:
    """
    Get the total number of bytes to fill, corresponding to the given QR code version and error correction level
    """
    codewords_table = pd.read_csv(Path(__file__).parent / "codewordsTable.csv")
    return codewords_table.loc[(codewords_table["Version"] == version) & (codewords_table["EC Level"] == error_correction_level.name), "Codewords"].squeeze()
