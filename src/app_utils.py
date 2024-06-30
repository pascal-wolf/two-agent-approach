from typing import Any, Dict, Generator, Iterable
import uuid
import streamlit as st


def stream_parser(
    stream: Iterable[Dict[str, Any]], model_type: str
) -> Generator[str, None, None]:
    """
    Parses a stream of dictionaries based on the model type.

    This function iterates over each dictionary in the stream. If the model type is 'ollama', it yields
    the content of the 'message'. If the model type is 'langchain', it checks if the dictionary contains
    the key 'answer' and if so, yields the value associated with this key. If the model type is neither
    'ollama' nor 'langchain', it raises a NotImplementedError.

    Parameters:
    stream (Iterable[Dict[str, Any]]): The stream of dictionaries to parse.
    model_type (str): The type of model that generated the stream.

    Returns:
    Generator[str, None, None]: A generator that yields the parsed content from the stream.
    """
    if model_type == "ollama":
        for chunk in stream:
            yield chunk["message"]["content"]
    elif model_type == "langchain":
        for chunk in stream:
            if "answer" in chunk.keys():
                yield chunk["answer"]
    else:
        raise NotImplementedError


def user_message(message: str, i: int) -> None:
    """
    Displays a user message in a Streamlit app with a select box for question type.

    This function creates two columns in the Streamlit app. It displays the message in the first column.
    In the second column, it displays a select box with options for "Quantitative", "Qualitative", and
    "Compound" question types. The select box has a unique key based on the input 'i' and its label is
    collapsed.

    Parameters:
    message (str): The message to be displayed.
    i (int): The unique key for the select box.

    Returns:
    None
    """
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(message)
    with col2:
        _ = st.selectbox(
            "Question Type",
            ("Quantitative", "Qualitative", "Compound"),
            key=i,
            label_visibility="collapsed",
        )


def assistent_message(message: str, i: int) -> None:
    """
    Displays a message in a Streamlit app with optional thumbs up and thumbs down buttons.

    This function creates three columns in the Streamlit app. It displays the message in the first column.
    If 'i' is not 0, it also displays a thumbs up button in the second column and a thumbs down button in
    the third column. Each button has a unique key generated using the uuid library.

    Parameters:
    message (str): The message to be displayed.
    i (int): If not 0, thumbs up and thumbs down buttons are displayed.

    Returns:
    None
    """
    col1, col2, col3 = st.columns([10, 1, 1])
    with col1:
        st.markdown(message)
    if i != 0:
        with col2:
            st.button("👍", key=uuid.uuid4())
        with col3:
            st.button("👎", key=uuid.uuid4())


def get_context(stream: Iterable[Dict[str, Any]]) -> Any:
    """
    Extracts the 'context' from a stream of dictionaries.

    This function iterates over each dictionary in the stream. If a dictionary contains the key 'context',
    it returns the value associated with this key.

    Parameters:
    stream (Iterable[Dict[str, Any]]): The stream of dictionaries to search for the 'context'.

    Returns:
    Any: The value associated with the 'context' key, or None if no such key is found.
    """
    for chunk in stream:
        if "context" in chunk.keys():
            return chunk["context"]
