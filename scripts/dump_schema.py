import pandas as pd

try:
    df = pd.read_excel('c:/Users/chowd/OneDrive/Desktop/DAE/data/raw/DAE Product Price Web Scraping Dataset 2000 Records final.xlsx')
    
    with open('c:/Users/chowd/OneDrive/Desktop/DAE/reports/schema.txt', 'w', encoding='utf-8') as f:
        f.write('HEAD:\n')
        f.write(df.head(5).to_string() + '\n\n')
        f.write('Columns: ' + str(df.columns.tolist()) + '\n\n')
        
        type_dict = {col: str(dtype) for col, dtype in df.dtypes.items()}
        f.write('Types: ' + str(type_dict) + '\n\n')
        f.write('Summary:\n')
        f.write(df.describe().to_string())
        
except Exception as e:
    with open('c:/Users/chowd/OneDrive/Desktop/DAE/reports/schema.txt', 'w', encoding='utf-8') as f:
        f.write(str(e))
