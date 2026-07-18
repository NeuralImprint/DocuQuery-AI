#pending and improvise
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ocr_database"]
collection = db["ocr_results"]

documents = list(collection.find())
import networkx as nx

G = nx.Graph()

for doc in documents:
    name = doc.get("Name")
    if name:
        G.add_node(name, type="Person")
        
       
        if "Age" in doc:
            G.add_node(doc["Age"], type="Age")
            G.add_edge(name, doc["Age"], relation="hasAge")
        
        if "Marks" in doc:
            G.add_node(doc["Marks"], type="Marks")
            G.add_edge(name, doc["Marks"], relation="hasMarks")

        if "Roll No" in doc:
            G.add_node(doc["Roll No"], type="RollNo")
            G.add_edge(name, doc["Roll No"], relation="hasRollNo")

print(list(G.neighbors("Amit")))


for u, v, data in G.edges(data=True):
    print(f"{u} --[{data['relation']}]--> {v}")
