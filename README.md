# Chat with your PDF - RAG with LangChain + Streamlit

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then add your OPENAI_API_KEY
streamlit run app.py
```

## Pipeline
PDF Upload -> Loader -> Text Extraction -> Chunking -> Embeddings ->
Vector Store (Chroma) -> Retriever -> Context -> Prompt -> LLM -> Answer

## Files
| File | Role |
|---|---|
| pdf_loader.py | Save upload, load pages, extract text |
| text_splitter.py | Split into overlapping chunks |
| embeddings.py | Embedding model |
| vector_store.py | Chroma store (unique collection per upload) |
| retriever.py | Top-k similarity search |
| prompt.py | Grounded prompt + "not found" fallback |
| llm.py | Prompt -> LLM -> parser chain |
| app.py | Streamlit UI |
