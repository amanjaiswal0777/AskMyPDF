"""
STEP 2 - CHUNKING
-----------------
Why chunk? An embedding of a whole page mixes many topics, and LLMs have
limited context. Small, focused chunks give more precise retrieval.

RecursiveCharacterTextSplitter tries to split on paragraphs first, then
lines, then sentences, then words - so chunks stay as meaningful as possible.

chunk_size    : max characters per chunk (too small = no context,
                too big = noisy retrieval). ~1000 is a good starting point.
chunk_overlap : characters shared between neighbouring chunks, so a sentence
                cut at a boundary still appears whole in one of them.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    # Give every chunk an id so the UI can label "Chunk #3"
    for i, chunk in enumerate(chunks, start=1):
        chunk.metadata["chunk_id"] = i

    return chunks
