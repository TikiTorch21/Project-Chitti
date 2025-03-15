import numpy as np
import Levenshtein
import pandas as pd

def levenshtein_distance(text1: str, text2: str) -> int:
    """
    Compute the Levenshtein distance between two strings.

    Args:
        text1 (str): The first string.
        text2 (str): The second string. 

    Returns:
        int: The Levenshtein distance between the two imput strings. 
    """
    return Levenshtein.distance(text1, text2)

def compute_similariy(df: pd.DataFrame, suffixes: list[str], similarity_fun: callable, col_prefix: str) -> pd.DataFrame:
    for suffix in suffixes:
        col_name = f'{col_prefix}_{suffix}'
        df[col_name] = df.apply(
            lambda x: similarity_fun(x['pageContent_actual'], x['pageContent_{suffix}']), axis=1
        )

    return df
