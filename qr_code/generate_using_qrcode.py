import qrcode


def generate(url: str, output_path: str = "test_output.png") -> None:
    """
    Generate the QR code corresponding to the given URL
    Stores it in a png file.
    """
    img = qrcode.make(url)
    img.save(output_path)
