"""
STEP 1 - DOCUMENT LOADER + TEXT EXTRACTION
-------------------------------------------
Streamlit gives us the uploaded PDF as an in-memory object, but PyPDFLoader
needs a file path. So we write the bytes to a temporary file, load it, and
delete the temp file. PyPDFLoader returns one `Document` per page, each with:
  - page_content : the extracted text
  - metadata     : {"source": ..., "page": <0-based page number>}
We keep that metadata so we can later show the user WHICH page a chunk came from.
"""
import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(uploaded_file):
    # Save the uploaded bytes to a temporary .pdf file on disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    try:
        documents = PyPDFLoader(tmp_path).load()  # one Document per page
    finally:
        os.remove(tmp_path)  # always clean up, even if loading fails

    # Drop pages with no text (blank pages / scanned images without OCR)
    documents = [d for d in documents if d.page_content.strip()]

    if not documents:
        raise ValueError(
            "No text could be extracted. The PDF may be scanned images "
            "(it would need OCR) or it may be empty."
        )

    # Replace the temp-file path in metadata with the real file name
    for doc in documents:
        doc.metadata["source"] = uploaded_file.name

    return documents
