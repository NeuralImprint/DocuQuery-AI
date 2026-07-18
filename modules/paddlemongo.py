from paddleocr import PPStructure
from pymongo import MongoClient
import pandas as pd

ocr_engine = PPStructure(
    layout=True,
    show_log=True,
    table=True,
    ocr=True,
    lang='en',
    structure_version='PP-StructureV2'
)
#change the connectionid as per sys

client = MongoClient("mongodb://localhost:27017/")
db = client["ocr_database"]
collection = db["ocr_results"]

image_path = "Excel.png"
print(f" Processing: {image_path}")
result = ocr_engine(image_path)

for res in result:
    if 'res' in res and isinstance(res['res'], list):
        table_data = res['res']
        rows = []

        for row in table_data:
            if isinstance(row, list):
                cells = [cell['text'] for cell in row if isinstance(cell, dict) and 'text' in cell]
                if cells:
                    rows.append(cells)

        
        if len(rows) >= 2:
            df = pd.DataFrame(rows[1:], columns=rows[0])  
            df['source_image'] = image_path 

            records = df.to_dict(orient='records')
            if records:
                collection.insert_many(records)
                print(f" Uploaded {len(records)} rows from {image_path} to MongoDB.")
            else:
                print(f" No valid records extracted from {image_path}.")
        else:
            print(f" Not enough table rows in {image_path} to build a DataFrame.")
