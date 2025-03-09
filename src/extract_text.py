from thefuzz import fuzz
from pathlib import Path
from pypdf import PdfReader
from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
import pymupdf
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt


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
    time_list = []
    for page_num in range(len(file.pages)):
        key = f'{str(file_path).split('/')[-1]} ~ {page_num}'
        start = time.time()
        extracted_txt = file.pages[page_num].extract_text()
        end = time.time()
        pdf_dict[key] = extracted_txt
        time_list.append(end-start)
    return pdf_dict, time_list


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
    time_list = []
    for page_num in range(file.page_count):
        start = time.time()
        text = file[page_num].get_text()
        end = time.time()
        pdf_dict[f'{str(file_path).split('/')[-1]} ~ {page_num}'] = text
        time_list.append(end-start)
    return pdf_dict, time_list


def pdfminersix_txt_extraction(file_path: Path) -> dict[str, str]:
    """
    Helper function to extract text from a pdf using pdfminer.six page-wise.

    Args:
        file_path: Path of the pdf file

    Returns:
        dict: key: page number, value: page text
    """
    pdf_dict = {}
    time_list = []
    with open(file_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        parser.set_document(doc)
        pages = resolve1(doc.catalog['Pages'])
        pages_count = pages.get('Count', 0)
    for page_num in range(pages_count):
        start = time.time()
        text = extract_text(file_path, page_numbers=[page_num])
        end = time.time()
        pdf_dict[f'{str(file_path).split('/')[-1]} ~ {page_num}'] = text
        time_list.append(end-start)
    return pdf_dict, time_list

def ground_truth(txt_path: Path) -> str:
    with open(txt_path) as file:
        ground_truth = file.read()
    return ground_truth


def create_dataframe(pypdf_output, pymupdf_output, pdfminer_output):
    pdf_df = pd.DataFrame({'PDF_ID': list(pypdf_output[0].keys())})
    #pdf_df['txt_actual'] = 
    pdf_df['txt_pypdf'] = list((pypdf_output[0]).values())
    pdf_df['txt_pymupdf'] = list((pymupdf_output[0]).values())
    pdf_df['txt_pdfminersix'] = list((pdfminer_output[0]).values())
    pdf_df['time_pypdf'] = list(pypdf_output[1])
    pdf_df['time_pymupdf'] = list(pymupdf_output[1])
    pdf_df['time_pdfminersix'] = list(pdfminer_output[1])
    return pdf_df

print(create_dataframe(
    pypdf_output=pypdf_txt_extraction(file_path=Path.cwd() / '../data/raw/test pdfs/chess_pdf.pdf'),
    pymupdf_output=pymupdf_txt_extraction(file_path=Path.cwd() / '../data/raw/test pdfs/chess_pdf.pdf'),
    pdfminer_output=pdfminersix_txt_extraction(file_path=Path.cwd() / '../data/raw/test pdfs/chess_pdf.pdf')
))

