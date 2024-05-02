def encode_data(url: str, mode: str) -> str:
    """
    Encode the data in bytes.
    """
    if mode != "Byte":
        raise ValueError("Only Byte mode is supported.")

    if not url.isascii():
        raise ValueError("ASCII characters only are supported.")
    return "".join(f"{ord(i):08b}" for i in url)
