import streamlit as st
import ollama
import uuid
from llm import rag_pipeline, classify_question, compound_answer


def stream_parser(stream, model_type):
    if model_type == "ollama":
        for chunk in stream:
            yield chunk["message"]["content"]
    elif model_type == "langchain":
        for chunk in stream:
            if "answer" in chunk.keys():
                yield chunk["answer"]
    else:
        raise NotImplementedError


def user_message(message, i):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(message)
    with col2:
        option = st.selectbox(
            "Question Type",
            ("Quantitative", "Qualitative", "Compound"),
            key=i,
            label_visibility="collapsed",
        )


def assistent_message(message, i):
    col1, col2, col3 = st.columns([10, 1, 1])
    with col1:
        st.markdown(message)
    if i != 0:
        with col2:
            st.button("👍", key=uuid.uuid4())
        with col3:
            st.button("👎", key=uuid.uuid4())


def get_context(stream):
    for chunk in stream:
        if "context" in chunk.keys():
            return chunk["context"]


if __name__ == "__main__":

    with st.sidebar:
        st.title("Context")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                assistent_message(msg["content"], i)
            else:
                user_message(msg["content"], i)

    if prompt := st.chat_input():
        # Display user prompt in chat message widget

        with st.chat_message("user"):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(prompt)
            with col2:
                question_class = classify_question(prompt)
                options = ["Quantitative", "Qualitative", "Compound"]
                option = st.selectbox(
                    "",
                    options,
                    label_visibility="collapsed",
                    index=options.index(question_class.capitalize()),
                )

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            if question_class.lower() == "compound":
                stream = compound_answer(prompt)
                context = []
                MODEL_TYPE = "ollama"
            else:
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
                st.divider()
