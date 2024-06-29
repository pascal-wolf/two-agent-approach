from typing import Any, Dict

import ollama
import pandas as pd
import redis
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.redis import Redis
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from redis.commands.search.query import Query

from config import REDIS_INDEX_NAME, REDIS_SCHEMA, REDIS_URL
from prompts import (
    CLASSIFICATION_PROMPT,
    COMPOUND_PROMPT,
    QUANTITATIVE_PROMPT,
    RAG_PIPELINE,
    REPHRASE_PROMPT,
)


redis_client = redis.Redis.from_url(REDIS_URL)
rs = redis_client.ft(REDIS_INDEX_NAME)


def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def quantitative_answer(question: str) -> Dict[str, Any]:
    """
    Generates a quantitative answer for a given question using the Ollama chat model.

    This function sends a chat request to the Ollama chat model with a system role message
    containing a predefined QUANTITATIVE_PROMPT and a user role message containing the question.

    It then extracts the content of the message from the chat model's response, replaces all
    parentheses with square brackets, and prints the query.

    If the query is not "na", it performs a search using the query and sets the total number
    of results as the answer. If the query is "na", it sets the answer as "na".

    It then rephrases the answer using the rephrase_answer function and returns the rephrased answer.

    Parameters:
    question (str): The question to be answered.

    Returns:
    Dict[str, Any]: The rephrased answer stream from the Ollama chat model.
    """
    query_dict = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": QUANTITATIVE_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )
    query = query_dict["message"]["content"].replace("(", "[").replace(")", "]")
    print(query)
    if query != "na":
        answer = rs.search(Query(query)).total
    else:
        answer = "na"
    stream = rephrase_answer(question, answer)
    return stream


def rephrase_answer(question: str, answer: str) -> Dict[str, Any]:
    """
    Rephrases a given answer using the Ollama chat model.

    This function sends a chat request to the Ollama chat model with a system role message
    containing a predefined REPHRASE_PROMPT and a user role message containing the question
    and answer in the format "Question: {question} Answer: {answer}". The chat model is set
    to stream the response.

    Parameters:
    question (str): The original question.
    answer (str): The original answer.

    Returns:
    Dict[str, Any]: The rephrased answer stream from the Ollama chat model.
    """
    stream = ollama.chat(
        model="llama3",
        stream=True,
        messages=[
            {
                "role": "system",
                "content": REPHRASE_PROMPT,
            },
            {
                "role": "user",
                "content": f"Question: {question} Answer: {answer}",
            },
        ],
    )
    return stream


def compound_answer(question: str) -> Dict[str, Any]:
    """
    Generates a compound answer for a given question using the Ollama chat model.

    This function sends a chat request to the Ollama chat model with a system role message
    containing a predefined COMPOUND_PROMPT and a user role message containing the question.
    The chat model is set to stream the response.

    Parameters:
    question (str): The question to be answered.

    Returns:
    Dict[str, Any]: The answer stream from the Ollama chat model.
    """
    stream = ollama.chat(
        model="llama3",
        stream=True,
        messages=[
            {
                "role": "system",
                "content": COMPOUND_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )
    return stream


def rag_pipeline() -> RunnableParallel:
    """
    Creates a RAG (Retrieval-Augmented Generation) pipeline using the Ollama chat model.

    This function first creates an embedder using the OllamaEmbeddings model. It then creates a vector store
    from an existing index in a Redis database using the embedder.

    It then creates a retriever from the vector store with a search parameter of 10.

    It creates a chat prompt template from a predefined RAG_PIPELINE template and a chat model using the
    ChatOllama model.

    It then creates a rag_chain_from_docs which is a sequence of operations that formats the context,
    applies the prompt, applies the model, and parses the output to a string.

    Finally, it creates a chain which is a parallel runnable that takes the retriever as the context and
    a passthrough as the question, and assigns the rag_chain_from_docs as the answer.

    Returns:
    RunnableParallel: The RAG pipeline.
    """
    embedder = OllamaEmbeddings(model="llama3")

    vectorstore = Redis.from_existing_index(
        embedding=embedder,
        index_name=REDIS_INDEX_NAME,
        schema=REDIS_SCHEMA,
        redis_url=REDIS_URL,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    prompt = ChatPromptTemplate.from_template(RAG_PIPELINE)

    model = ChatOllama(model="llama3")

    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: _format_docs(x["context"])))
        | prompt
        | model
        | StrOutputParser()
    )

    chain = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)
    return chain


def create_embeddings(df: pd.DataFrame) -> None:
    """
    Creates embeddings for a given DataFrame using the Ollama chat model.

    Parameters:
    df (pd.DataFrame): The DataFrame for which to create embeddings.

    This function modifies the input DataFrame by converting the 'created_date' and
    'contains_source_word' columns to string type. It then creates a list of all columns
    except 'content' and converts these columns to a list of dictionaries.

    It also creates a list of all 'content' in the DataFrame.

    It then creates embeddings for the first 1000 texts and corresponding metadata using
    the OllamaEmbeddings model and stores them in a Redis database.

    Finally, it writes the schema to the Redis database.
    """
    embeddings = OllamaEmbeddings(model="llama3")
    df["created_date"] = df["created_date"].apply(str)
    df["contains_source_word"] = df["contains_source_word"].apply(str)

    metadata_columns = df.columns.tolist()
    metadata_columns.remove("content")
    metadata = df[metadata_columns].to_dict("records")
    texts = df["content"].tolist()

    rds = Redis.from_texts(
        texts[:1000],
        embeddings,
        metadatas=metadata[:1000],
        redis_url=REDIS_URL,
        index_name=REDIS_INDEX_NAME,
    )
    rds.write_schema(REDIS_SCHEMA)


def classify_question(question: str) -> str:
    """
    Classifies a question using the Ollama chat model.

    Parameters:
    question (str): The question to be classified.

    Returns:
    str: The classification result from the Ollama chat model.
    """
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": CLASSIFICATION_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )
    return response["message"]["content"]
