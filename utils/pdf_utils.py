from pathlib import Path

def pypdf_txt_extraction(file_path: Path) -> dict[str, str]:
    """
    Helper function to extract text from a pdf using pypdf page-wise.

    Args:
        file_path: Path of the pdf file

    Returns:
        dict: key: page number, value: page text
    """
    pass

def pymupdf_txt_extraction(file_path: Path) -> dict[str, str]:
    """
    Helper function to extract text from a pdf using pymupdf page-wise.

    Args:
        file_path: Path of the pdf file

    Returns:
        dict: key: page number, value: page text
    """
    pass

def pdfminersix_txt_extraction(file_path: Path) -> dict[str, str]:
    """
    Helper function to extract text from a pdf using pdfminer.six page-wise.

    Args:
        file_path: Path of the pdf file

    Returns:
        dict: key: page number, value: page text
    """
    pass
