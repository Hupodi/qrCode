from pathlib import Path

import pandas as pd


def get_character_count(url: str, version: int, mode: str = "Byte") -> str:
    """
    From the input URL and the version, get the character count indicator.
    Should also depend on the mode, but we're supporting bytes only.
    """
    bits_count_table = pd.read_csv(Path(__file__).parent / "characterCountTable.csv")

    bits_count = bits_count_table.loc[
            bits_count_table["Version"] == version, mode
        ].squeeze()

    return f"{len(url):0{bits_count}b}"
