"""
Streamlit UI for AI Support Desk.

Phase 5 responsibilities:
- Chat interface
- Call FastAPI backend
- Display responses
- Simulated streaming output
"""

import time
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/chat"

# -------------------------
# Page setup
# -------------------------

st.set_page_config(page_title="AI Support Desk", layout="centered")
st.title("🛠️ AI Support Desk")

st.write(
    "Ask about customers, tickets, support policies, or general information."
)

# -------------------------
# Session state
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Chat display
# -------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# User input
# -------------------------

user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call backend
    try:
        response = requests.post(
            API_URL,
            json={"message": user_input},
            timeout=60,
        )
        response.raise_for_status()
        answer = response.json()["answer"]

    except requests.exceptions.Timeout:
        answer = "Error: The request timed out. Please try again."
    except Exception as e:
        answer = f"Error: {str(e)}"

    # Simulated streaming output
    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed_text = ""

        for token in answer.split(" "):
            streamed_text += token + " "
            placeholder.markdown(streamed_text)
            time.sleep(0.03)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
