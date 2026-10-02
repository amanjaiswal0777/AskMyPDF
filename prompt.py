"""
STEP 6 - PROMPT CONSTRUCTION
----------------------------
The prompt is what turns "an LLM" into "a RAG system". It:
  - tells the model to answer ONLY from the retrieved context (reduces hallucination)
  - gives an exact fallback sentence when the answer is missing
  - injects the retrieved chunks and the user's question
"""
from langchain_core.prompts import ChatPromptTemplate

NOT_FOUND_MESSAGE = "The information is not available in the uploaded PDF."

SYSTEM_PROMPT = f"""You are a helpful assistant that answers questions about a PDF document.

Rules:
1. Use ONLY the context below. Do not use outside knowledge.
2. Judge whether information is present by meaning, not by exact wording. The context may describe an answer without using the same words as the question.
3. If any retrieved context is relevant, answer from the relevant parts. For broad requests such as summaries or lists, use all the provided context. If only part of the request is supported, answer that part and briefly say what is missing.
4. Reply exactly "{NOT_FOUND_MESSAGE}" only when the context is empty or none of it is relevant to the question.
5. Follow the format and number of items requested by the user. If the user asks for bullet points, use bullets; provide the requested count when the context supports it.
6. For a requested list, make each item a distinct idea supported by the context. Do not repeat points or invent information to reach the requested count. If the context supports fewer items, give the supported items and say that the context does not support more.
7. Be clear and concise. Mention page numbers when helpful.
8. Never invent facts that are not in the context.

Context:
{{context}}"""

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ]
)


def format_context(docs):
    """Join retrieved chunks into one string, labelled with their page numbers."""
    parts = []
    for doc in docs:
        page = doc.metadata.get("page", 0) + 1  # PyPDF pages start at 0
        parts.append(f"[Page {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)
