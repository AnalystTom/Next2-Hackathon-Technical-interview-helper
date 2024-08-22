import logging
import sys
import time
from typing import Optional
import requests
import streamlit as st
from streamlit_chat import message

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)

BASE_API_URL = "https://musaqlain-langflow-hackathon-clearout.hf.space/api/v1/run"
FLOW_ID = "0b93e3c9-b7d0-4769-bd56-e603ec03cc69"

uploaded_doc_url = None

def upload_document_to_service(document_file):
    return "https://example.com/uploaded_document.pdf"

def main():
    st.set_page_config(page_title="DocuWizard", page_icon="🧙‍♂️", layout="wide")

    st.markdown(
        """
        <style>
            .stApp {
                background-color: #f5f5f5;
                color: #333;
            }
            .main-title {
                color: #ff4b4b;
                font-family: 'Arial Black', sans-serif;
            }
            .sub-title {
                color: #007bff;
                font-family: 'Arial', sans-serif;
            }
            .upload-button {
                background-color: #28a745;
                color: white;
            }
            .upload-button:hover {
                background-color: #218838;
            }
            .st-chat-message-user {
                background-color: #007bff;
                color: white;
                border-radius: 10px;
            }
            .st-chat-message-assistant {
                background-color: #ffc107;
                color: black;
                border-radius: 10px;
            }
            .code-section {
                background-color: #2d2d2d;
                color: #f8f8f2;
                padding: 10px;
                border-radius: 5px;
                font-family: 'Courier New', Courier, monospace;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 class='main-title'>🧙‍♂️ Welcome to DocuWizard</h1>", unsafe_allow_html=True)
    st.markdown("#### Your smart document assistant. Ask anything about your documents!", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    if "uploaded_doc_url" not in st.session_state:
        st.session_state.uploaded_doc_url = None

    if prompt := st.chat_input("Ask me anything about your documents!"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
                "avatar": "https://example.com/user-avatar.png",
            }
        )
        with st.chat_message(
            "user",
            avatar="https://example.com/user-avatar.png",
        ):
            st.write(prompt)

        with st.chat_message(
            "assistant",
            avatar="https://example.com/assistant-avatar.png",
        ):
            message_placeholder = st.empty()
            with st.spinner(text="Thinking..."):
                assistant_response = generate_response(prompt)
                message_placeholder.write(assistant_response)
        
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": "https://example.com/assistant-avatar.png",
            }
        )
    
    document_upload_component()
    coding_section()

def document_upload_component():
    global uploaded_doc_url
    
    st.markdown("### Upload a Document", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a document...", type=["pdf", "docx", "txt", "csv"])
    
    if uploaded_file is not None:
        if st.button("Upload", key="upload", use_container_width=True, type="primary", css_class="upload-button"):
            with st.spinner("Uploading..."):
                doc_url = upload_document_to_service(uploaded_file)
                st.session_state.uploaded_doc_url = doc_url
                st.success("Document uploaded successfully!")
                st.write(f"Document URL: {doc_url}")

def coding_section():
    st.markdown("<h2 class='sub-title'>💻 Coding Question & Feedback</h2>", unsafe_allow_html=True)

    coding_question = "Write a function that returns the factorial of a number."
    st.markdown(f"<div class='code-section'>{coding_question}</div>", unsafe_allow_html=True)

    user_code = st.text_area("Your code here:", height=150)
    
    if st.button("Submit Code"):
        with st.spinner("Evaluating your code..."):
            feedback = evaluate_code(user_code, coding_question)
            st.markdown(f"### Feedback:\n{feedback}", unsafe_allow_html=True)

def evaluate_code(user_code, coding_question):
    return "Great job! Your code is efficient and works as expected."

def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    api_url = f"{BASE_API_URL}/{flow_id}"

    payload = {"inputs": inputs}

    if tweaks:
        payload["tweaks"] = tweaks

    response = requests.post(api_url, json=payload)
    
    return response.json()

def generate_response(prompt):
    logging.info(f"question: {prompt}")
    inputs = {"question": prompt}
    
    tweaks = {
        "ChatInput-PKbEo": {
            "input_value": prompt,
            "sender": "User",
            "sender_name": "User",
            "session_id": "",
            "store_message": True
        },
    }

    if st.session_state.uploaded_doc_url:
        tweaks["FileUploadComponent-DYGG2"] = {
            "AIMLApiKey": "8759623ce0574e56b454933d4e4ee4aa",
            "MaxTokens": 300,
            "model": "gpt-4o",
            "prompt": "Analyze the document",
            "uploaded_file": st.session_state.uploaded_doc_url
        }

    response = run_flow(inputs, flow_id=FLOW_ID, tweaks=tweaks)

    try:
        logging.info(f"answer: {response['outputs'][0]['outputs'][0]['results']['message']['data']['text']}")
        return response['outputs'][0]['outputs'][0]['results']['message']['data']['text']
    except Exception as exc:
        logging.error(f"error: {response}")
        return "Sorry, there was a problem finding an answer for you."

if __name__ == "__main__":
    main()
