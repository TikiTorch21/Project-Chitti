import pandas as pd
from pathlib import Path
import numpy as np

def merge_csvs(path1: str, path2: str) -> pd.DataFrame:
    """
    Reads two CSV files from the given paths, converts them into DataFrames,
    and merges them on the 'pdfId' column.

    Parameters:
        path1 (str): File path to the first CSV.
        path2 (str): File path to the second CSV.

    Returns:
        pd.DataFrame: A merged DataFrame on 'pdfId'.
    """

    extractions_df = pd.read_csv(path1)
    ground_truth_df = pd.read_csv(path2)
    left_col = [col for col in extractions_df.columns if 'pdfId' in col][0]


    print(left_col)
    return pd.merge(extractions_df, ground_truth_df, left_on=left_col, right_on='pdfId', how='inner')  



TXT_EXTRACTION_PATH = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions')

final_df = merge_csvs(TXT_EXTRACTION_PATH / 'consolidated_extractions.csv', TXT_EXTRACTION_PATH / 'ground_truth_txt_extractions.csv')
final_df.to_csv(TXT_EXTRACTION_PATH / 'final_consolidated.csv', index=None)