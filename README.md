# AskMyPDF

> Upload a PDF, ask questions in plain English, and get answers grounded in the document with the source passages shown alongside.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-LLM-black)

## Overview

**AskMyPDF** is a Retrieval-Augmented Generation (RAG) application that allows users to upload a PDF and ask questions about its content.

Instead of asking the language model to answer from memory, the application:

1. Loads the PDF
2. Splits the document into smaller chunks
3. Converts the chunks into embeddings
4. Stores them in a vector database
5. Retrieves the most relevant chunks for a user's question
6. Sends the retrieved context to the LLM
7. Generates an answer based only on the retrieved information

If the document does not contain the answer, the application responds:

> The information is not available in the uploaded PDF.

---

## Features

- Upload a text-based PDF
- Process the PDF with one click
- Automatically split the PDF into chunks
- Generate embeddings using OpenAI
- Store embeddings in ChromaDB
- Ask questions about the uploaded document
- Retrieve the most relevant chunks
- Generate answers using an LLM
- Display the retrieved context used to generate the answer
- Show page numbers and chunk IDs
- Configure chunk size and chunk overlap
- Configure the number of retrieved chunks (`k`)
- Select the LLM model
- Create a fresh vector store for every uploaded PDF

---

## RAG Pipeline

```text
PDF Upload
    ↓
Document Loader
    ↓
Text Chunking
    ↓
Embeddings
    ↓
ChromaDB Vector Store
    ↓
Retriever
    ↓
Relevant Chunks
    ↓
Prompt
    ↓
LLM
    ↓
Answer + Retrieved Context
