#from thefuzz import fuzz
from pathlib import Path
from pypdf import PdfReader
from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
import pymupdf
import pandas as pd
import numpy as np 

def pypdf_txt_extraction(file_path: Path) -> dict[str, str]:
    """
    Helper function to extract text from a pdf using pypdf page-wise.

    Args:
        file_path: Path of the pdf file

    Returns:
        dict: key: page number, value: page text
    """
    pdf_dict = {}
    file = PdfReader(file_path)
    for page_num in range(len(file.pages)):
        pdf_dict[f'{str(test_pdf).split('/')[-1]} ~ {page_num}'] = file.pages[page_num].extract_text()
    return pdf_dict

def pymupdf_txt_extraction(file_path: Path) -> dict[str, str]:
    """
    Helper function to extract text from a pdf using pymupdf page-wise.

    Args:
        file_path: Path of the pdf file

    Returns:
        dict: key: page number, value: page text
    """
    file = pymupdf.open(file_path)
    pdf_dict = {}
    for page_num in range(file.page_count):
        text = file[page_num].get_text()
        pdf_dict[f'{str(file_path).split('/')[-1]} ~ {page_num}'] = text
    return pdf_dict

def pdfminersix_txt_extraction(file_path: Path) -> dict[str, str]:
    """
    Helper function to extract text from a pdf using pdfminer.six page-wise.

    Args:
        file_path: Path of the pdf file

    Returns:
        dict: key: page number, value: page text
    """
    test_path = PDF_FILES_PATH / 'chess_pdf.pdf'
    pdf_dict = {}
    with open(test_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        parser.set_document(doc)
        pages = resolve1(doc.catalog['Pages'])
        pages_count = pages.get('Count', 0)
    for page_num in range(pages_count):
        text = extract_text(test_path, page_numbers=[page_num])
        pdf_dict[f'{str(test_path).split('/')[-1]} ~ {page_num}'] = text
    return pdf_dict

def pdf_dataframe(pdf_dict1: dict, pdf_dict2: dict, pdfdict3: dict) -> DataFrame:
    pass