import pandas as pd
import numpy as np
from pathlib import Path 


pypdf_path = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions/pypdf/pypdf_txt_extractions.csv')
pymupdf_path = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions/pymupdf/pymupdf_txt_extractions.csv')
pdfminer_path = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions/pdfminer.six/pdfminer_txt_extractions.csv')

# pypdf_df = pd.read_csv(pypdf_path)
# pymupdf_df = pd.read_csv(pymupdf_path)


# df = pd.concat([pypdf_df, pymupdf_df], axis='columns')

# df.to_csv(output_path / 'test_concat.csv')

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
        df = df.loc[:, ~df.columns.str.contains('path', case=False)]  # note TO SELF: Essentially saying keep the columns without 'path', because ~ means negate. Case means not case senstive.
        merged_df = pd.concat([merged_df, df], axis='columns', join='outer')

    merged_df.to_csv(output_path)

concat_pdf_txt_extractions(pypdf_path, pymupdf_path, pdfminer_path, output_path='/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions/consolidated_extractions.csv')
