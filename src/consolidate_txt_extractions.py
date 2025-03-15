from utils import pdf_utils

def consolidate_txt_extractions(pdf_paths, output_pdf_path):
    pypdf_dict, pypdf_time = pdf_utils.pymupdf_txt_extraction()