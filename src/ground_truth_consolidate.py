import pandas as pd
from pathlib import Path
import numpy as np
from utils.metrics import *

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



    final_df = pd.merge(extractions_df, ground_truth_df, left_on=left_col, right_on='pdfId', how='inner')
    return final_df.drop('content_actual', axis=1)

TXT_EXTRACTION_PATH = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions')

ground_truth_final = merge_csvs(TXT_EXTRACTION_PATH / 'consolidated_extractions.csv', TXT_EXTRACTION_PATH / 'ground_truth_txt_extractions.csv')


def add_library_similarity_scores(df, extraction_cols):
    d = {
        '1': 'pypdf',
        '2': 'pymupdf',
        '3': 'pdfminer'
    }
    
    for idx, col in enumerate(extraction_cols, start=1):
        df[f'{d[str(idx)]}_bleu'] = df.apply(
            lambda row: bleu_score(row[col], row['text']), axis=1
        )
        df[f'{d[str(idx)]}_jaccard'] = df.apply(
            lambda row: jaccard_similarity(row[col], row['text']), axis=1
        )
        df[f'{d[str(idx)]}_levenshtein'] = df.apply(
            lambda row: levenshtein_distance(row[col], row['text']), axis=1
        )
    return df
extraction_cols = ['pageContent_pypdf', 'pageContent_pymupdf', 'pageContent_pdfminer']
final_df = add_library_similarity_scores(ground_truth_final, extraction_cols)
final_df.to_csv(TXT_EXTRACTION_PATH / 'final_consolidated.csv', index=None)