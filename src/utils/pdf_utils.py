#from thefuzz import fuzz
import pymupdf
import time


def extract_pdf_text(file_path, extraction_func):
    """Generic function that would work with all PDF libraries"""
    extracted_data = []


    for page_no, page_content in enumerate(extraction_func(file_path)):
        extracted_data.append(
            {
                'path': file_path,
                'pageNumber': page_no,
                'pdfId': f"{str(file_path).split('/')[-1]} ~ {page_no}",
                'pageContent': page_content['text'],
                'extractionTimeSeconds': page_content['extraction_time']
            }
        )

    return extracted_data

def pymupdf_extract_page_text(pdf):
    """
    Function to extract text from a PDF using pymupdf
    
    Parameters
    ----------
    pdf : str
        Path to a PDF file
    
    Returns
    -------
    list
        A list of dictionaries, each containing the extracted text and extraction time 
        for each page in the PDF
    """
    page_by_page = []
    doc = pymupdf.open(pdf)

    for page in doc:
        start_time = time.time()
        page_text = page.get_text()
        extraction_time = time.time() - start_time
        page_by_page.append({'text': page_text, 'extraction_time': extraction_time})

    return page_by_page


def pymupdf_extract_pdf_text(pdf):
    """
    Function to extract text from a PDF using pymupdf
    
    Parameters
    ----------
    pdf : str
        Path to a PDF file
    
    Returns
    -------
    list
        A list of dictionaries, each containing the extracted text and extraction time 
        for each page in the PDF
    """
    return extract_pdf_text(pdf, pymupdf_extract_page_text)