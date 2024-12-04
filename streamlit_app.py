import os
import tempfile

import streamlit as st
from rag import PDFChatbot
from streamlit_chat import message

st.set_page_config(page_title="ChatPDF")

def display_chat_messages():
    """Display chat messages in the chat window."""
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["chat_messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()

def handle_user_input():
    """Handle the user input and display assistant response."""
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_message = st.session_state["user_input"].strip()
        st.session_state["chat_messages"].append((user_message, True))
        with st.session_state["thinking_spinner"], st.spinner("Processing your question..."):
            assistant_response = st.session_state["pdf_chatbot"].answer_question(user_message)
        st.session_state["chat_messages"].append((assistant_response, False))

def upload_and_process_file():
    """Upload and process the PDF file, then update chatbot index."""
    pdf_chatbot: PDFChatbot = st.session_state["pdf_chatbot"]
    pdf_chatbot.reset()
    st.session_state["chat_messages"] = []
    st.session_state["user_input"] = ""

    for uploaded_file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            file_path = temp_file.name

        with st.session_state["processing_spinner"], st.spinner(f"Indexing {uploaded_file.name}..."):
            st.session_state["pdf_chatbot"].load_and_index_pdf(file_path)
        os.remove(file_path)

def main_page():
    """Set up the main page of the Streamlit app."""
    if 'pdf_chatbot' not in st.session_state:
        st.session_state["pdf_chatbot"] = PDFChatbot()
        st.session_state["chat_messages"] = []
        st.session_state["user_input"] = ""

    st.sidebar.header("Upload Your PDF Document")
    st.sidebar.file_uploader(
        "Choose a PDF file to upload",
        type="pdf",
        key="file_uploader",
        on_change=upload_and_process_file,
        label_visibility="collapsed",
        accept_multiple_files=True
    )

    st.session_state["processing_spinner"] = st.empty()

    st.title("ChatPDF")
    display_chat_messages()
    st.text_input("Type your question here...", key="user_input", on_change=handle_user_input)

if __name__ == "__main__":
    main_page()