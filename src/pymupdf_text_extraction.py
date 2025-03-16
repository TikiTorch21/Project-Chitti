import pandas as pd
from pathlib import Path
from pprint import pprint

from utils.pdf_utils import pymupdf_extract_pdf_text

def text_extract(pdf_dir):
    all_pdf_text = [
        pymupdf_extract_pdf_text(pdf) for pdf in pdf_dir
    ]

    #pprint(all_pdf_text[:2])
    
    flat_texts = [
        each_page_dict
        for each_pdf_list in all_pdf_text
        for each_page_dict in each_pdf_list
    ]
    pprint(flat_texts)
    df = pd.DataFrame(
        flat_texts,
        columns = ['path', 'pageNumber', 'pdfId', 'pageContent', 'extractionTimeSeconds']
    )

    return df

PROJECT_PATH = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti')
PDF_PATH = (PROJECT_PATH / 'data' / 'raw' / 'test pdfs').glob('*.pdf')

pdf_df = text_extract(PDF_PATH)
pdf_df.to_csv(PROJECT_PATH / 'data' / 'text extractions' / 'pymupdf' / 'pymupdf_txt_extractions.csv', index=None)