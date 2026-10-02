"""
STEP 3 - EMBEDDINGS
-------------------
An embedding turns text into a list of numbers (a vector) such that texts with
similar MEANING get vectors that are close together. This is what lets us
search by meaning instead of by exact keywords.

IMPORTANT: the same embedding model must be used for the chunks AND for the
user's question, otherwise the vectors live in different "spaces" and the
similarity comparison is meaningless.
"""
from langchain_openai import OpenAIEmbeddings


def get_embedding_model(model_name="text-embedding-3-small"):
    return OpenAIEmbeddings(model=model_name)
