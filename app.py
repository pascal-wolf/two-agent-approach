import uuid

import streamlit as st
from PIL import Image

from llm import (
    classify_question,
    compound_answer,
    quantitative_answer,
    rag_pipeline,
)
from src.app_utils import (
    assistent_message,
    get_context,
    stream_parser,
    user_message,
)


if __name__ == "__main__":

    st.set_page_config(
        page_title="Reviews Chat",
        page_icon=Image.open("favicon.ico"),
    )

    with st.sidebar:
        st.title("Context")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "Hello! I'm a chatbot capable of answering both qualitative and quantitative questions about reviews from Spotify, ChatGPT, and Netflix!",
            }
        ]

    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                assistent_message(msg["content"], i)
            else:
                user_message(msg["content"], i)

    if prompt := st.chat_input():
        with st.chat_message("user"):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(prompt)
            with col2:
                question_class = classify_question(prompt)
                options = ["Quantitative", "Qualitative", "Compound"]
                option = st.selectbox(
                    "Question Type",
                    options,
                    label_visibility="collapsed",
                    index=options.index(question_class.capitalize()),
                )

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            if question_class.lower() == "compound":
                MODEL_TYPE = "ollama"
                stream = compound_answer(prompt)
                context = []
            elif question_class.lower() == "quantitative":
                MODEL_TYPE = "ollama"
                stream = quantitative_answer(prompt)
                context = []
            elif question_class.lower() == "qualitative":
                chain = rag_pipeline()
                stream = chain.stream(input=prompt)
                context = get_context(stream)
                MODEL_TYPE = "langchain"

            col1, col2, col3 = st.columns([10, 1, 1])
            with col1:
                answer = st.write_stream(stream_parser(stream, model_type=MODEL_TYPE))
            with col2:
                st.button("👍", key=uuid.uuid4())
            with col3:
                st.button("👎", key=uuid.uuid4())

            st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.sidebar:
            st.divider()
            for i, document in enumerate(context):
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.write(document.page_content)
                    st.markdown(
                        f"***Reviewed at {document.metadata['created_date']}***"
                    )
                    st.markdown(f"***{document.metadata['likes']} likes***")
                st.divider()
