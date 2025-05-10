import numpy as np
import Levenshtein
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction


from nltk.metrics import edit_distance

def levenshtein_distance(extraction, ground_truth) -> int:
    # Ensure both extraction and ground_truth are strings, and handle None or non-string types
    extraction = str(extraction)
    ground_truth = str(ground_truth)
    
    # Calculate the Levenshtein distance
    return edit_distance(extraction, ground_truth)

def bleu_score(extraction, ground_truth) -> float:
    # Ensure both extraction and ground_truth are strings, and handle None or non-string types
    extraction = str(extraction)
    ground_truth = str(ground_truth)
    
    reference = [ground_truth.split()]  # Ground truth is a list of words
    candidate = extraction.split()      # Extracted text is a list of words
    smoothie = SmoothingFunction().method1  # Smoothing to avoid zero probabilities
    
    # Return the BLEU score
    return sentence_bleu(reference, candidate, smoothing_function=smoothie)



def jaccard_similarity(extraction, ground_truth) -> float:
    # Ensure both extraction and ground_truth are strings, and handle None or non-string types
    extraction = str(extraction)
    ground_truth = str(ground_truth)
    
    # Convert the strings to sets of words
    extraction_set = set(extraction.split())
    ground_truth_set = set(ground_truth.split())
    
    # Calculate Jaccard similarity: |Intersection| / |Union|
    intersection = len(extraction_set.intersection(ground_truth_set))
    union = len(extraction_set.union(ground_truth_set))
    
    # If the union is 0 (i.e., both sets are empty), return 0 to avoid division by zero
    return intersection / union if union != 0 else 0.0


