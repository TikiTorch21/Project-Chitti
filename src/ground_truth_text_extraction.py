from pathlib import Path
import pandas as pd
import numpy as np 
import re
def ground_truth_text_extraction(txt_path: Path) -> pd.DataFrame:
    data = [] 
    for idx, path in enumerate(txt_path.glob('*.txt'), start=1):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split on <page n> markers
        pages = re.split(r'<page\s*\d+\s*>', content, flags=re.IGNORECASE)
        pages = [page for page in pages if page]
        # pdf_names = [str(path).split('/')[-1].replace('.txt', '.pdf')] * len(pages)
        pdf_names = path.stem + '.pdf'
        for page_no, page_text in enumerate(pages, start=1):
            data.append({'pdfId': f'{pdf_names} ~ {page_no}', 'text': page_text })
        # for pdf_name, page_text in zip(pdf_names, pages): 
        #     data.append({'id': f'{pdf_name} ~ {idx}', 'text': page_text })

    df = pd.DataFrame(data) 
    return df

OUTPUT_PATH = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/text extractions')
GROUND_TRUTH = Path('/Users/prateekM/Downloads/Coding/Classes/Projects/Project Chitti/data/raw/ground truth')

df = ground_truth_text_extraction(GROUND_TRUTH)
df.to_csv(OUTPUT_PATH / 'ground_truth_txt_extractions.csv', index=None)