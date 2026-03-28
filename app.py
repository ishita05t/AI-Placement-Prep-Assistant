import streamlit as st
import os
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# ─────────────────────────────────────────
# LLM
# ─────────────────────────────────────────
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

# ─────────────────────────────────────────
# PROMPT
# ─────────────────────────────────────────
prompt_template = """
You are an AI Placement Prep Assistant helping students prepare for job interviews.
Answer the question based on the provided context from interview preparation materials.
Be specific, structured, and give examples where possible.
If the answer is not in the context, say "I don't have enough information on this topic in the loaded documents."

<context>
{context}
</context>

Question: {input}
"""
prompt = ChatPromptTemplate.from_template(prompt_template)

# ─────────────────────────────────────────
# VECTOR EMBEDDING
# ─────────────────────────────────────────
def vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        loader = PyPDFDirectoryLoader("./data")
        docs = loader.load()
        if not docs:
            st.error("No PDFs found in ./data folder. Please upload some PDFs first.")
            return
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        final_documents = text_splitter.split_documents(docs)
        st.session_state.vectors = FAISS.from_documents(
            final_documents,
            st.session_state.embeddings
        )

# ─────────────────────────────────────────
# CHAT MEMORY INIT
# ─────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="AI Placement Prep Assistant",
    page_icon="💼",
    layout="wide"
)

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.title("💼 Placement Prep")
    st.markdown("---")

    # ── File Upload ──
    st.markdown("### 📤 Upload PDFs")
    uploaded_files = st.file_uploader(
        "Upload interview PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        os.makedirs("./data", exist_ok=True)
        saved = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join("./data", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            saved.append(uploaded_file.name)
        st.success(f"✅ Saved {len(saved)} file(s) to ./data")
        for name in saved:
            st.write(f"  - `{name}`")

    st.markdown("---")

    # ── Show existing PDFs ──
    st.markdown("### 📁 Loaded Documents")
    if os.path.exists("./data"):
        pdf_files = [f for f in os.listdir("./data") if f.endswith(".pdf")]
        if pdf_files:
            for f in pdf_files:
                st.write(f"  - `{f}`")
        else:
            st.caption("No PDFs yet. Upload some above.")
    else:
        st.caption("No PDFs yet. Upload some above.")

    st.markdown("---")

    # ── Process Button ──
    st.markdown("### ⚙️ Data Management")
    if st.button("🔄 Process & Embed Documents", use_container_width=True):
        # Reset vectors so re-embedding happens fresh
        if "vectors" in st.session_state:
            del st.session_state["vectors"]
        with st.spinner("Embedding documents... this may take a minute."):
            vector_embedding()
        if "vectors" in st.session_state:
            st.success("✅ Ready! Ask your questions.")

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.memory.clear()
        st.success("Chat cleared!")

    st.markdown("---")

    # ── Sample Questions ──
    st.markdown("### 📌 Sample Questions")
    st.markdown("""
    - What are common HR interview questions?
    - Explain system design for a URL shortener
    - What is the difference between BFS and DFS?
    - How do I answer "Tell me about yourself"?
    - What are Amazon leadership principles?
    """)

# ─────────────────────────────────────────
# MAIN UI
# ─────────────────────────────────────────
st.title("💼 AI Placement Prep Assistant")
st.caption("Your AI-powered interview preparation assistant with explainable retrieval and conversational memory.")
st.markdown("---")

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        with st.chat_message("user"):
            st.write(chat["content"])
    else:
        with st.chat_message("assistant"):
            st.write(chat["content"])
            if "sources" in chat:
                with st.expander("📄 View Sources"):
                    for source in chat["sources"]:
                        st.write(f"- `{source}`")

# ─────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────
prompt1 = st.chat_input("Ask an interview-related question...")

if prompt1:
    if "vectors" not in st.session_state:
        st.warning("⚠️ Please upload PDFs and click '🔄 Process & Embed Documents' first.")
    else:
        with st.chat_message("user"):
            st.write(prompt1)

        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt1
        })

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                conversational_chain = ConversationalRetrievalChain.from_llm(
                    llm=llm,
                    retriever=st.session_state.vectors.as_retriever(
                        search_kwargs={"k": 4}
                    ),
                    memory=st.session_state.memory,
                    return_source_documents=True,
                    verbose=False
                )

                start = time.process_time()
                response = conversational_chain.invoke({"question": prompt1})
                elapsed = time.process_time() - start

                answer = response["answer"]
                source_docs = response.get("source_documents", [])

                sources = list(set([
                    os.path.basename(doc.metadata.get("source", "Unknown"))
                    for doc in source_docs
                ]))

                st.write(answer)
                st.caption(f"⏱️ Response time: {elapsed:.2f}s")

                with st.expander("📄 View Sources"):
                    for source in sources:
                        st.write(f"- `{source}`")

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })