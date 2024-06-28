from langchain_community.vectorstores.redis import Redis
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
from langchain_community.chat_models import ChatOllama

from prompts import RAG_PIPELINE


def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def rag_pipeline(prompt):
    embedder = OllamaEmbeddings(model="llama3")

    vectorstore = Redis.from_existing_index(
        embedding=embedder,
        index_name="reviews-main",
        schema="redis_schema.yaml",
        redis_url="redis://localhost:6379",
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    prompt = ChatPromptTemplate.from_template(RAG_PIPELINE)

    # RAG Chain
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


def create_embeddings(df):
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
        redis_url="redis://localhost:6379",
        index_name="reviews-main-v5",
    )
    rds.write_schema("redis_schema_v5.yaml")


# stream = ollama.chat(
#     model="llama3",
#     messages=[{"role": "user", "content": "Why is the sky blue?"}],
#     stream=True,
# )

# for chunk in stream:
#     print(chunk["message"]["content"], end="", flush=True)
