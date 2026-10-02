"""
STEP 5 - RETRIEVER
------------------
The retriever takes the user's question, embeds it with the same embedding
model (done automatically by the vector store), and returns the top-k most
similar chunks.

k controls the trade-off:
  small k -> precise but may miss information
  large k -> more complete but more noise and more LLM tokens
"""


def get_retriever(vectorstore, k=15):
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )


def retrieve_context(retriever, question):
    return retriever.invoke(question)  # list[Document]
