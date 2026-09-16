import pandas as pd
import json

try:
    file_path = 'c:/Users/chowd/OneDrive/Desktop/DAE/data/raw/DAE Product Price Web Scraping Dataset 2000 Records final.xlsx'
    df = pd.read_excel(file_path)
    
    info = {
        "num_rows": df.shape[0],
        "num_cols": df.shape[1],
        "columns": df.columns.tolist(),
        "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_records": int(df.duplicated().sum())
    }
    
    with open('c:/Users/chowd/OneDrive/Desktop/DAE/reports/inspection_results.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=4)
        
except Exception as e:
    with open('c:/Users/chowd/OneDrive/Desktop/DAE/reports/inspection_results.json', 'w', encoding='utf-8') as f:
        json.dump({"error": str(e)}, f, indent=4)
