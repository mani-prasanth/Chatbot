
import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Streamlit configuration
st.set_page_config(
    page_title="Prasanth Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Prasanth Chatbot")

# Cache Gemini client to prevent closing during Streamlit reruns
@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("gemini_api_key")

    if not api_key:
        raise ValueError("Gemini API key not found in .env file")

    return genai.Client(api_key=api_key)


# Initialize Gemini client
try:
    client = get_gemini_client()
except Exception as e:
    st.error(f"Gemini initialization failed: {e}")
    st.stop()


# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.5-flash-lite"
    )

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:
    st.header("Settings")

    if st.button("🗑️ New Chat", use_container_width=True):
        st.session_state.chat = client.chats.create(
            model="gemini-3.5-flash-lite"
        )
        st.session_state.messages = []
        st.rerun()


# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
user_input = st.chat_input("Ask me anything...")

if user_input:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Gemini response
    with st.chat_message("assistant"):

        with st.spinner("Bot is generating..."):

            try:
                response = st.session_state.chat.send_message(
                    user_input
                )

                bot_response = response.text or "No response received."

                st.markdown(bot_response)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_response
                })

            except Exception as e:
                st.error(f"Error while calling Gemini API: {e}")
