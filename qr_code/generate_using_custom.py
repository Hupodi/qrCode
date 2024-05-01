from .custom_generator import qr_generator, plot_png


def generate(url: str, output_path: str = "test_output.png") -> None:
    """
    Generate the QR code corresponding to the given URL
    Stores it in a png file.
    """
    matrix = qr_generator(url)
    plot_png(matrix=matrix, output_file=output_path)
