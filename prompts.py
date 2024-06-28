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

CLASSIFICATION_PROMPT = """
You are given a question and have to classify it into one of the following categories:
- Quantitative: Questions that can be answered with a number or a measurement.
- Qualitative: Questions that can be answered with a description or an opinion.
- Compound: Questions that contain not only one but multiple questions like for example a quantitative and a qualitative question seperated by the word 'and'.

Examples:
- quantitative: How many people are there in the world?
- qualitative: What is the best movie you have ever seen?
- compound: How many people are there in the world and what is the best movie you have ever seen?

Only reply with one word: quantitative, qualitative, compound. With no spaces or other characters.

User: 
"""

COMPOUND_PROMPT = """
You are given a question from a user. This question is a compound question, meaning it contains multiple questions.
Please tell the user that currently we only support one question at a time and suggest the user how he/she can split the question into multiple single questions.
Stay with the same questions the user asked and don't change the meaning of the questions.
"""
