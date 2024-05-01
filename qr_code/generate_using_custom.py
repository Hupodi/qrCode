from .custom_generator import generate_qr_code, plot_png


def generate(url: str, output_path: str = "test_output.png") -> None:
    """
    Generate the QR code corresponding to the given URL
    Stores it in a png file.
    """
    matrix = generate_qr_code(url)
    plot_png(matrix=matrix, output_file=output_path)
