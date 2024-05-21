from qr_code.custom_generator import generate_qr_code, plot_png
from qr_code.custom_generator.qr_generator.error_correction_level import ErrorCorrectionLevel


def generate(url: str, output_path: str = "test_output2.png") -> None:
    """
    Generate the QR code corresponding to the given URL
    Stores it in a png file.
    """
    matrix = generate_qr_code(url=url, error_correction_level=ErrorCorrectionLevel.L)
    plot_png(matrix=matrix, output_file=output_path)
