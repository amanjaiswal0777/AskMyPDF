"""
STEP 7 - LLM RESPONSE GENERATION
--------------------------------
We build a small LangChain "chain" using the | operator (LCEL):

    prompt  ->  LLM  ->  output parser

temperature=0 makes the model as deterministic/factual as possible, which is
what we want for question answering over documents.
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from prompt import NOT_FOUND_MESSAGE, format_context, prompt_template


def get_llm(model_name="gpt-4o-mini"):
    return ChatOpenAI(model=model_name, temperature=0)


def generate_answer(question, docs, llm):
    # Guard: nothing retrieved -> don't call the LLM at all
    if not docs:
        return NOT_FOUND_MESSAGE

    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke(
        {
            "context": format_context(docs),
            "question": question,
        }
    )
