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

def pypdf_txt_extraction(file_path: Path):
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
        start = time.time()
        extracted_txt = file.pages[page_num].extract_text()
        if extracted_txt:  # Avoiding None values
            pdf_dict[page_num] = extracted_txt
        end = time.time()
        time_list.append((page_num, end-start))
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

def create_pdf_from_selected_pages(input_pdf_path, output_pdf_path, selected_pages):
    """
    Create a new PDF from selected pages of an existing PDF.
    
    Handles both sequential and non-sequential page subsets.
    
    Parameters:
        input_pdf_path: The file path of the input PDF.
        output_pdf_path: The file path where the new PDF will be saved.
        selected_pages: A list of integers specifying the pages to extract (1-based index).
        
    Raises:
        ValueError: If selected pages are invalid or out of range.
        FileNotFoundError: If the input file is not found.
    """
    # Open the existing PDF
    try:
        input_pdf = pymupdf.open(input_pdf_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{input_pdf_path}' does not exist.")

    # Validate selected pages
    if not selected_pages or not all(isinstance(page, int) and page > 0 for page in selected_pages):
        input_pdf.close()
        raise ValueError("Selected pages must be a non-empty list of positive integers (1-based index).")

    # Ensure pages are unique and sorted
    selected_pages = sorted(set(selected_pages))

    # Check if pages are within range
    max_pages = len(input_pdf)
    if any(page > max_pages for page in selected_pages):
        input_pdf.close()
        raise ValueError(
            f"Some selected pages are out of range. Input PDF has {max_pages} pages."
        )

    # Create a new PDF document
    output_pdf = pymupdf.open()

    try:
        if is_sequential(selected_pages):
            # If pages are sequential, extract them in one go
            start_index = selected_pages[0] - 1  # Convert to 0-based index
            end_index = selected_pages[-1] - 1
            output_pdf.insert_pdf(input_pdf, from_page=start_index, to_page=end_index)
        else:
            # If pages are non-sequential, process individually
            for page_number in selected_pages:
                page_index = page_number - 1  # Convert to 0-based index
                output_pdf.insert_pdf(input_pdf, from_page=page_index, to_page=page_index)

        # Save the new PDF to the specified output path
        output_pdf.save(output_pdf_path)
        print(f"New PDF created successfully: {output_pdf_path}")
    except Exception as e:
        raise ValueError(f"An error occurred while processing pages: {e}")
    finally:
        # Close the documents
        input_pdf.close()
        output_pdf.close()


def is_sequential(pages):
    """
    Check if a list of pages is sequential. EG: [11, 12, 13, 14] is sequential.
    
    Parameters:
        pages: A sorted list of page numbers.
    
    Returns:
        bool: True if the pages are sequential, False otherwise.
    """
    return all(pages[i] + 1 == pages[i + 1] for i in range(len(pages) - 1))