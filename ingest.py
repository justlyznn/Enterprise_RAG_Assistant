import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores.pgvector import PGVector
from langchain_huggingface import HuggingFaceEmbeddings

# Connect to the DB exposed to the host machine
db_url = "postgresql://myuser:mypassword@127.0.0.1:5434/customer_db"

print("Loading dataset...")
df = pd.read_csv('data/dataset_assignment.csv')
df = df.dropna()

documents = []
# Ambil 2000 data acak agar semua kategori keluhan terwakili
subset_df = df.sample(n=2000, random_state=42)

for index, row in subset_df.iterrows():
    text = f"Q: {row['instruction']}\nA: {row['response']}"
    doc = Document(page_content=text, metadata={"id": index})
    documents.append(doc)

print(f"Total documents: {len(documents)}")

print("Loading embeddings model...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
collection_name = "customer_intelligence_kb_multi"

print("Ingesting to PgVector...")
vector_store = PGVector.from_documents(
    embedding=embeddings,
    documents=documents,
    collection_name=collection_name,
    connection_string=db_url,
    pre_delete_collection=True
)
print("Ingestion complete. Verifying...")

# Verify
import psycopg2
conn = psycopg2.connect("host=127.0.0.1 port=5434 user=myuser password=mypassword dbname=customer_db")
cur = conn.cursor()
cur.execute("SELECT count(*) FROM langchain_pg_embedding;")
print("Total embeddings in DB:", cur.fetchone()[0])
conn.close()
