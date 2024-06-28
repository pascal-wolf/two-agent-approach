RAG_PIPELINE = """
Use the following pieces of context from the review datasets from the spotify app, chatgpt app and netflix app
to answer the question. Do not make up an answer if there is no
context provided to help answer it.
Do not just repeat what it says in the context, but use the context to help you answer the question.
Context:
---------
{context}

---------
Question: {question}
---------

Answer:
"""
