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
Stay with the same questions the user asked and don't change the meaning of the questions. Only write the suggested questions one time.
"""

QUANTITATIVE_PROMPT = """
Given the following Redis database schema. Please return a query that can answer the question.
Examples are:

User question: How many users have the name Paul and are between 30 and 40 years old?
Answer from you: @user:Paul @age:[30 40]

User question: How many users are named Paul?
Answer from you:  @user:Paul

User question: How many reviews have more than 10 likes?
Answer from you: @likes:[10 +inf]

The correct syntax for a text and numeric question is the following:
text_field @numeric_field:[value_numeric_field]

Please always only return with the query! If you can't come up with a query only return the following two letters: na



The database schema is the following:
numeric:
- name: score
  no_index: false
  sortable: false
- name: likes
  no_index: false
  sortable: false
- name: likes_weighted
  no_index: false
  sortable: false
text:
- name: created_date
  no_index: false
  no_stem: false
  sortable: false
  weight: 1
  withsuffixtrie: false
- name: weekday
  no_index: false
  no_stem: false
  sortable: false
  weight: 1
  withsuffixtrie: false
- name: contains_source_word
  no_index: false
  no_stem: false
  sortable: false
  weight: 1
  withsuffixtrie: false
- name: content
  no_index: false
  no_stem: false
  sortable: false
  weight: 1
  withsuffixtrie: false
"""

REPHRASE_PROMPT = """
Your only task is to formulate an answer based on the user question and answer you got:
Make sure that you are specifically mentioning the number. If the answer is 'na' then please tell the user, that unfortunately,
you couldn't come up with a response and ask him/her to reformualte the question.
Only write the answer and do not say that you are now reformulating it!
"""
