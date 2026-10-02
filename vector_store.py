"""
STEP 4 - VECTOR STORE
---------------------
A vector store saves (chunk text, chunk vector, metadata) and can quickly
find the vectors closest to a query vector. We use Chroma.

Chroma.from_documents() does two things for us:
  1. calls the embedding model on every chunk
  2. stores the vectors + original text + metadata

We give each upload a UNIQUE collection name. Without this, chunks from a
previously uploaded PDF would stay in the store and answers could mix
content from different documents.
"""
import uuid

from langchain_chroma import Chroma


def create_vector_store(chunks, embeddings):
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=f"pdf_{uuid.uuid4().hex}",
        # No persist_directory -> stored in memory, fine for a single session.
        # Add persist_directory="./chroma_db" to keep data between runs.
    )


def delete_vector_store(vectorstore):
    """Free the old collection when the user processes a new PDF."""
    try:
        vectorstore.delete_collection()
    except Exception:
        pass
