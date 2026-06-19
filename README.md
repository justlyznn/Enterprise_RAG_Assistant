# Intelligent Customer Assistant System

Sistem asisten chatbot customer service end-to-end yang dibangun menggunakan **RAG (Retrieval-Augmented Generation)** dengan Langchain, Groq LLM, dan PgVector. Proyek ini memisahkan arsitektur menjadi 3 komponen utama: Data/Notebook, Backend (FastAPI), dan Frontend (Streamlit), yang diorkestrasi menggunakan Docker.

## Struktur Proyek
- `data/`: Folder untuk dataset `.csv`
- `notebooks/`: Jupyter notebook untuk *preprocessing* teks dan menyisipkan vector embeddings ke PgVector.
- `api/`: Aplikasi FastAPI untuk melayani permintaan pencarian semantic dan *generation* LLM.
- `ui/`: Antarmuka interaktif Streamlit untuk mengobrol dengan asisten.

## Cara Menjalankan (Lokal)

1. **Setup Lingkungan**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Kredensial API**
   Salin `.env.example` ke `.env` dan tambahkan `GROQ_API_KEY` Anda.

3. **Data Ingestion**
   - Jalankan database melalui docker: `docker-compose up -d db`
   - Buka `notebooks/preprocessing_and_embedding.ipynb` dan jalankan semua cell untuk memasukkan data dari CSV ke dalam PostgreSQL (PgVector).

4. **Menjalankan Sistem**
   Untuk menjalankan sistem secara lengkap (API + UI):
   ```bash
   docker-compose up --build
   ```

5. Buka `http://localhost:8501` untuk melihat chatbot UI.
