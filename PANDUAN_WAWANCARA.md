# 📚 Panduan Portofolio & Wawancara: Enterprise RAG Assistant

Dokumen ini dirancang khusus untuk membantu Anda memahami keseluruhan proyek secara mendalam, sehingga Anda dapat menjelaskannya dengan sangat lancar dan meyakinkan saat sesi wawancara kerja (HR atau Technical Interview).

---

## 🌟 1. Ringkasan Eksekutif Proyek (Elevator Pitch)
**"Apa proyek yang Anda buat?"**
> *"Saya membangun sistem Intelligent Customer Assistant berbasis AI. Sistem ini bukan chatbot biasa, melainkan menggunakan arsitektur **Retrieval-Augmented Generation (RAG)** skala Enterprise. AI ini mampu menjawab keluhan pelanggan berdasarkan basis pengetahuan perusahaan secara akurat, mendukung multibahasa (Indonesia & Inggris), dan seluruh komponennya (Database, Backend API, Frontend UI) dijalankan secara independen menggunakan **Docker**."*

---

## 🏗️ 2. Arsitektur & Teknologi (Tech Stack)
Proyek ini sengaja dibangun menggunakan konsep **Microservices** (terpisah-pisah) agar mirip dengan sistem di perusahaan besar:

1. **Database Layer (PostgreSQL + PgVector):** 
   - Menyimpan *knowledge base* (aturan perusahaan, FAQ). 
   - PgVector digunakan untuk menyimpan "vektor matematika" dari teks, sehingga pencarian mirip-makna (Semantic Search) bisa dilakukan.
2. **Backend/API Layer (FastAPI):**
   - Jantung logika aplikasi. Menghubungkan *database* dengan *Model AI*.
   - Menggunakan **Langchain** sebagai kerangka kerja RAG.
   - Menggunakan **Groq (Llama 3)** sebagai "otak" pintar yang merangkai kata.
3. **Frontend/UI Layer (Chainlit):**
   - Antarmuka *chat* modern yang cantik dan sangat interaktif layaknya ChatGPT.
4. **Orkestrasi (Docker Compose):**
   - Mengikat ketiga sistem di atas agar bisa dijalankan dengan satu perintah (`docker-compose up`) di komputer mana pun tanpa *error*.

---

## ⚙️ 3. Bagaimana Data Diproses? (Data Pipeline)
Data awal berasal dari *Bitext Customer Support Dataset* (Kaggle). Prosesnya:
1. **Pembersihan:** Menghapus baris kosong (`dropna`).
2. **Restrukturisasi:** Menggabungkan kolom "Instruksi" dan "Respons" menjadi satu teks berformat `Q & A`.
3. **Sampling:** Mengambil 2.000 sampel acak secara representatif agar sistem ringan tapi tetap memuat semua variasi kasus keluhan.
4. **Embedding (Penerjemahan Teks ke Vektor):** Teks bahasa manusia diubah menjadi deretan angka (vektor) menggunakan model **`paraphrase-multilingual-MiniLM-L12-v2`**, lalu disimpan ke PostgreSQL.

---

## 🎯 4. Nilai Jual Utama (Key Selling Points)
Sebutkan poin-poin ini di CV atau saat wawancara untuk membuat *recruiter* kagum:
- **Multilingual RAG:** Pengguna bisa bertanya dalam **Bahasa Indonesia**, sistem akan secara ajaib mencari aturan perusahaan dalam **Bahasa Inggris** di *database*, lalu menjawab kembali dalam **Bahasa Indonesia**.
- **Enterprise-Grade Infrastructure:** Tidak menggunakan SQLite/ChromaDB lokal, melainkan *dedicated database server* (PostgreSQL).
- **Blazing Fast AI:** Menggunakan *Groq LPU* (salah satu penyedia *chip* AI tercepat di dunia saat ini) yang dipadukan dengan Llama-3.

---

## 🗣️ 5. Simulasi Tanya Jawab Wawancara (Q&A)

Berikut adalah 3 pertanyaan teknis yang paling sering ditanyakan oleh *Tech Lead* atau *Senior Engineer*, beserta cara elegan menjawabnya:

> **Pertanyaan 1: "Mengapa Anda menggunakan PostgreSQL (PgVector) ketimbang *vector database* yang lebih instan seperti ChromaDB atau FAISS?"**
> 
> **Jawaban Anda:** 
> *"Saya memilih PostgreSQL dengan ekstensi PgVector karena lebih mencerminkan dunia industri nyata (Enterprise ready). Di perusahaan asli, data pelanggan dan log transaksi biasanya sudah ada di *Relational Database* seperti Postgres. Dengan PgVector, saya bisa melakukan pencarian semantik (AI) dan filter tradisional (SQL) di dalam satu database yang sama, tanpa perlu repot sinkronisasi data ke *database* lain. Selain itu, PostgreSQL memiliki skalabilitas, keamanan, dan *backup* yang sudah sangat matang."*

---

> **Pertanyaan 2: "Bagaimana cara sistem Anda mengatasi *query* atau pertanyaan dari *user* berbahasa Indonesia, padahal data asli perusahaan (FAQ) menggunakan bahasa Inggris?"**
> 
> **Jawaban Anda:** 
> *"Saya mengatasi masalah tersebut dengan mengimplementasikan model embedding **Multilingual** (`paraphrase-multilingual-MiniLM-L12-v2`). Model ini sangat canggih karena memetakan kata dalam bahasa Indonesia (misal: 'mengembalikan') ke dalam titik koordinat vektor yang persis sama dengan padanan bahasa Inggrisnya ('return'). Sehingga, RAG pipeline saya berhasil menarik konteks FAQ berbahasa Inggris yang tepat. Konteks tersebut kemudian diumpankan ke Llama-3 yang diperintahkan untuk merespons dengan bahasa asli pengguna."*

---

> **Pertanyaan 3: "Coba jelaskan secara singkat alur dari saat *user* mengetik di UI hingga balasan muncul!"**
> 
> **Jawaban Anda:** 
> *"Tentu. Alurnya seperti ini:*
> *1. User mengetik pesan di UI (Chainlit).*
> *2. Chainlit mengirim pesan itu via HTTP API ke Backend (FastAPI).*
> *3. Di FastAPI, teks *user* diubah menjadi vektor (Embedding).*
> *4. Vektor tersebut dikirim ke PgVector untuk mencari 3 dokumen FAQ perusahaan yang maknanya paling mirip (Cosine Similarity).*
> *5. Dokumen yang ditemukan tersebut disisipkan sebagai 'Konteks Rahasia' bersamaan dengan pertanyaan awal user.*
> *6. Semuanya dikirim ke LLM (Groq Llama 3) beserta *system prompt* ketat agar ia menjawab murni berdasarkan konteks.*
> *7. LLM menghasilkan jawaban cerdas yang langsung dikembalikan (*stream*) ke UI Chainlit."*

> **Pertanyaan 4: "Aplikasi kamu bagus, tapi kenapa tidak di-deploy ke cloud (seperti Vercel atau Streamlit Cloud) agar saya/penguji bisa langsung mencobanya secara online?"**
> 
> **Jawaban Anda:** 
> *"Ada tiga alasan utama secara teknis dan bisnis mengapa proyek ini saya desain untuk berjalan secara lokal dengan Docker:*
> *1. **Arsitektur Enterprise:** Sistem ini terdiri dari 3 kontainer terpisah (Database Postgres, FastAPI, dan UI). Platform gratisan seperti Streamlit Cloud hanya bisa menjalankan 1 file UI, tidak sanggup menjalankan *Vector Database* dan API secara bersamaan.*
> *2. **Efisiensi Biaya (Cost-Awareness):** Untuk men-deploy arsitektur Docker Compose secara penuh selama 24/7, saya membutuhkan server VPS atau layanan Cloud berbayar. Sebagai praktisi yang sadar akan efisiensi biaya perusahaan, saya memilih menunjukkan kemampuan saya membangun arsitektur 'Siap-Deploy' (menggunakan Docker) ketimbang membakar biaya server.*
> *3. **Keamanan Data:** Di perusahaan nyata, data pelanggan tidak boleh sembarangan diunggah ke cloud publik gratisan. Jika Bapak/Ibu ingin mengujinya sekarang, saya bisa menjalankannya di laptop saya dan membuka **Tunneling Aman** (via Pinggy/Ngrok) agar Bapak/Ibu bisa mengaksesnya secara live dari HP/Laptop Anda saat ini juga."*

---
*Persiapkan dokumen ini, baca berulang-ulang, dan Anda akan tampil seperti seorang AI Engineer profesional di wawancara mana pun! Selamat berjuang!* 🚀
