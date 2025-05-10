import pandas as pd
import numpy as np
from pathlib import Path 


pypdf_path = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions/pypdf/pypdf_txt_extractions.csv')
pymupdf_path = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions/pymupdf/pymupdf_txt_extractions.csv')
pdfminer_path = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions/pdfminer.six/pdfminer_txt_extractions.csv')
ground_truth_path = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions/ground_truth_txt_extractions.csv')

def concat_pdf_txt_extractions(*pdf_paths, output_path) -> None:
    """
    Concatenate multiple PDF text extraction CSVs into one.

    Parameters
    ----------
    *pdf_paths : Path
        Paths to the PDF text extraction CSVs.
    output_path : Path
        Path to save the final concatenated CSV.

    Returns
    -------
    None
    """
    merged_df = pd.DataFrame()

    for csv_path in pdf_paths:
        df = pd.read_csv(csv_path)
        df.drop(list(df.filter(regex='path').columns), axis=1, inplace=True)
        merged_df = pd.concat([merged_df, df], axis='columns', join='outer')
    
    merged_df.drop(['pageNumber_pymupdf', 'pageNumber_pdfminer', 'pdfId_pymupdf', 'pdfId_pdfminer'], axis=1, inplace=True)
    merged_df.to_csv(output_path)

concat_pdf_txt_extractions(pypdf_path, pymupdf_path, pdfminer_path, ground_truth_path,output_path='/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions/consolidated_extractions.csv')