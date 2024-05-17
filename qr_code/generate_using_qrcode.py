import qrcode


def generate(url: str, output_path: str = "test_with_package.png") -> None:
    """
    Generate the QR code corresponding to the given URL
    Stores it in a png file.
    """
    img = qrcode.make(url, error_correction=qrcode.constants.ERROR_CORRECT_L)
    img.save(output_path)
