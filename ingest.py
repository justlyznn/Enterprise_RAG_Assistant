import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores.pgvector import PGVector
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

# Connect to the DB from environment variables
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL tidak ditemukan di .env!")

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

print("Ingesting to PgVector (Supabase)...")
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
conn = psycopg2.connect(db_url)
cur = conn.cursor()
cur.execute("SELECT count(*) FROM langchain_pg_embedding;")
print("Total embeddings in DB:", cur.fetchone()[0])
conn.close()
