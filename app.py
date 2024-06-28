import streamlit as st
import ollama
import uuid
from llm import rag_pipeline


def stream_parser(stream):
    for chunk in stream:
        if "answer" in chunk.keys():
            yield chunk["answer"]


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


if __name__ == "__main__":

    with st.sidebar:
        st.title("Context")

    st.title("Reviews Chat")

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
                option = st.selectbox(
                    "",
                    ("Quantitative", "Qualitative", "Compound"),
                    label_visibility="collapsed",
                )

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            # stream = ollama.chat(
            #     model="llama3",
            #     messages=st.session_state.messages,
            #     stream=True,
            # )
            chain = rag_pipeline(prompt)
            stream = chain.stream(input="What positive do people think about the apps?")

            col1, col2, col3 = st.columns([10, 1, 1])
            with col1:
                with st.spinner("Thinking..."):
                    stream_output = st.write_stream(stream_parser(stream))
            with col2:
                st.button("👍", key=uuid.uuid4())
            with col3:
                st.button("👎", key=uuid.uuid4())

            # assistent_message(stream_output, -1)

            st.session_state.messages.append(
                {"role": "assistant", "content": stream_output}
            )
