"""
STREAMLIT UI - ties all the modules together.

Run with:  streamlit run app.py

Streamlit re-runs this whole script on every click, so anything we want to
keep (vector store, answer, retrieved chunks) lives in st.session_state.
"""
import os

import streamlit as st
from dotenv import load_dotenv

from embeddings import get_embedding_model
from llm import generate_answer, get_llm
from pdf_loader import load_pdf
from retriever import get_retriever, retrieve_context
from text_splitter import split_documents
from vector_store import create_vector_store, delete_vector_store

load_dotenv()  # reads OPENAI_API_KEY from the .env file

st.set_page_config(page_title="Chat with your PDF", page_icon="📄", layout="wide")
st.title("📄 Chat with your PDF (RAG)")
st.caption("Upload a PDF, process it, then ask questions about its content.")

# ---- Fail early and clearly if the API key is missing -----------------------
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY not found. Create a `.env` file (see `.env.example`).")
    st.stop()

# ---- Session state defaults -------------------------------------------------
for key, default in {
    "vectorstore": None,
    "pdf_name": None,
    "num_pages": 0,
    "num_chunks": 0,
    "answer": "",
    "retrieved_docs": [],
}.items():
    st.session_state.setdefault(key, default)

# ---- Sidebar: tunable settings ---------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    chunk_size = st.slider("Chunk size (characters)", 300, 2000, 1000, 100)
    chunk_overlap = st.slider("Chunk overlap", 0, 500, 200, 50)
    top_k = st.slider("Chunks to retrieve (k)", 1, 20, 15)
    llm_model = st.selectbox("LLM model", ["gpt-4o-mini", "gpt-4o"])
    st.info("Chunk settings apply the next time you click **Process PDF**.")

# ---- Section 1: Upload + process -------------------------------------------
st.subheader("1️⃣ Upload and process your PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if st.button("Process PDF", type="primary"):
    if uploaded_file is None:
        st.warning("Please upload a PDF first.")
    else:
        try:
            with st.spinner("Reading PDF, chunking, creating embeddings..."):
                # Remove the previous PDF's data so answers never mix documents
                if st.session_state.vectorstore is not None:
                    delete_vector_store(st.session_state.vectorstore)

                documents = load_pdf(uploaded_file)                       # load + extract
                chunks = split_documents(documents, chunk_size, chunk_overlap)  # chunk
                embeddings = get_embedding_model()                        # embed model
                vectorstore = create_vector_store(chunks, embeddings)     # embed + store

            st.session_state.update(
                vectorstore=vectorstore,
                pdf_name=uploaded_file.name,
                num_pages=len(documents),
                num_chunks=len(chunks),
                answer="",
                retrieved_docs=[],
            )
            st.success("PDF processed! You can now ask questions.")
        except Exception as e:
            st.error(f"Could not process the PDF: {e}")

if st.session_state.vectorstore is not None:
    c1, c2, c3 = st.columns(3)
    c1.metric("Document", st.session_state.pdf_name)
    c2.metric("Pages with text", st.session_state.num_pages)
    c3.metric("Chunks stored", st.session_state.num_chunks)

st.divider()

# ---- Section 2: Ask a question ---------------------------------------------
st.subheader("2️⃣ Ask a question")
question = st.text_area(
    "Your question",
    placeholder="e.g. What are the main conclusions of this document?",
    height=100,
)

if st.button("Ask Question"):
    if st.session_state.vectorstore is None:
        st.warning("Please upload and process a PDF first.")
    elif not question.strip():
        st.warning("Please type a question.")
    else:
        try:
            with st.spinner("Searching the document and generating an answer..."):
                retriever = get_retriever(st.session_state.vectorstore, k=top_k)
                docs = retrieve_context(retriever, question)    # retrieve
                answer = generate_answer(question, docs, get_llm(llm_model))  # generate
            st.session_state.answer = answer
            st.session_state.retrieved_docs = docs
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---- Section 3: Answer ------------------------------------------------------
st.subheader("3️⃣ Answer")
st.text_area(
    "Generated answer",
    value=st.session_state.answer,
    height=220,
    disabled=True,
    label_visibility="collapsed",
)

# ---- Section 4: Retrieved context ------------------------------------------
st.subheader("4️⃣ Retrieved context")
if st.checkbox("Show retrieved context / chunks"):
    if not st.session_state.retrieved_docs:
        st.info("Ask a question to see which chunks were retrieved.")
    for i, doc in enumerate(st.session_state.retrieved_docs, start=1):
        page = doc.metadata.get("page", 0) + 1
        chunk_id = doc.metadata.get("chunk_id", "?")
        with st.expander(f"Result {i} • Page {page} • Chunk #{chunk_id}", expanded=(i == 1)):
            st.write(doc.page_content)
