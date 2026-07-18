import pandas as pd
df = pd.read_excel("Hand_table.xlsx") 
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["ocr_database"]
collection = db["ocr_results"]

data_dict = df.to_dict(orient="records")

collection.insert_many(data_dict)

print("Data inserted successfully!")

for doc in collection.find().limit(5):
    print(doc)
def upload_to_mongo(file_path, db_name, collection_name):
    df = pd.read_excel(file_path)
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]
    data_dict = df.to_dict(orient="records")
    collection.insert_many(data_dict)
    print("Upload complete!")

#ensure kro same files in app.py
upload_to_mongo("Hand_table.xlsx", "ocr_database", "ocr_results")

