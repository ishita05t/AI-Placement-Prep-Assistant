# 💼 AI Placement Prep Assistant

> An AI-powered interview preparation assistant with explainable retrieval and conversational memory — built using RAG architecture.

![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.3.25-green?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-red?style=flat-square&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-purple?style=flat-square)
![License](https://img.shields.io/badge/License-GPL%20v3-yellow?style=flat-square)

---

## 🚀 About The Project

**AI Placement Prep Assistant** is a RAG-based (Retrieval-Augmented Generation) application that lets students upload their own interview preparation PDFs — such as HR question banks, DSA notes, system design guides, and company-specific prep material — and ask questions conversationally, just like ChatGPT.

The system retrieves relevant chunks from the uploaded documents and generates accurate, context-grounded answers using the **Groq LLaMA 3.1** model — with source attribution showing exactly which document the answer came from.

---

## ✨ Features

- 📄 **Multi-PDF Upload** — Upload multiple interview prep PDFs directly from the browser
- 🔍 **Semantic Search** — HuggingFace embeddings + FAISS vector store for accurate retrieval
- 🧠 **Conversational Memory** — Remembers previous questions in the session (true chat memory)
- 📌 **Source Citation** — Shows which document each answer came from
- ⚡ **Fast Responses** — Powered by Groq's LLaMA 3.1 8B Instant model
- 💬 **ChatGPT-style UI** — Clean chat bubble interface built with Streamlit
- ⏱️ **Response Time Tracking** — Shows how long each answer took

---

## 🏗️ Architecture

```
PDF Documents
     │
     ▼
┌─────────────────┐
│  PDF Loader     │  ← PyPDFDirectoryLoader
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Chunker   │  ← RecursiveCharacterTextSplitter
│  chunk=1000     │     overlap=200
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Embeddings     │  ← HuggingFace all-MiniLM-L6-v2
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector Store   │  ← FAISS (local)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Retriever      │  ← Top-4 relevant chunks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM            │  ← Groq LLaMA 3.1 8B Instant
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Answer +       │  ← Displayed in Streamlit UI
│  Source Docs    │     with chat memory
└─────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Groq — LLaMA 3.1 8B Instant |
| Embeddings | HuggingFace — all-MiniLM-L6-v2 |
| Vector Store | FAISS |
| Framework | LangChain |
| Memory | ConversationBufferMemory |
| PDF Loader | PyPDFDirectoryLoader |
| Environment | Python 3.13 |

---

## 📁 Project Structure

```
ai-placement-prep-assistant/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed)
├── .gitignore
├── data/                   # Uploaded PDFs (not committed)
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.13
- A [Groq API Key](https://console.groq.com/keys) (free)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ishita05t/ai-placement-prep-assistant.git
cd ai-placement-prep-assistant
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\Activate.ps1      # Windows
source venv/bin/activate        # Mac/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up your API key**

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the app**
```bash
streamlit run app.py
```

---

## 🎯 How To Use

1. **Upload PDFs** — Use the sidebar to upload your interview prep PDFs (HR questions, DSA notes, company guides, etc.)
2. **Process Documents** — Click **"🔄 Process & Embed Documents"** to embed them into the vector store
3. **Ask Questions** — Type any interview-related question in the chat input
4. **View Sources** — Expand **"📄 View Sources"** under each answer to see which document it came from

### Example PDFs to upload
- Amazon Interview Questions
- System Design Notes
- Behavioral Questions Guide
- DSA Cheat Sheet
- Company-specific Prep Docs

---

## 📝 Resume Bullet

> Built an AI-powered placement preparation assistant using RAG architecture (LangChain + FAISS + Groq LLaMA 3.1) to enable contextual Q&A over multi-document datasets, with source attribution and conversational memory.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.

---

## 👩‍💻 Author

**Ishita Tegar**

[![GitHub](https://img.shields.io/badge/GitHub-ishita05t-181717?style=flat-square&logo=github)](https://github.com/ishita05t)

---

⭐ If you found this project helpful, please give it a star!
