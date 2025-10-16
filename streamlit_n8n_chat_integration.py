import streamlit as st
import requests
import json
import time
import uuid # 🚨 NEW: Import UUID library for reliable session ID generation

# ==============================================================================
# CONFIGURATION
# 🚨 IMPORTANT: This URL is TEMPORARY and valid only while your ngrok terminal 
# is running. Replace it with your permanent cloud URL when deploying n8n.
# ==============================================================================
N8N_WEBHOOK_URL = "https://libbie-semidramatic-cesar.ngrok-free.dev/webhook/970120ca-bb27-4bcd-805f-87f4a331b2a1/chat" 

st.set_page_config(page_title="n8n-Powered Product Concierge", layout="centered")

# --- UI Header ---
st.title("🛍️ Product Concierge Chatbot")
st.caption("Powered by n8n AI Agent, Pinecone RAG, and Google Sheets (Lead Capture).")

# ==============================================================================
# SESSION STATE AND MEMORY MANAGEMENT (FIXED)
# ==============================================================================

# 1. Initialize Chat History
if "messages" not in st.session_state:
    # Start with the initial greeting defined in your n8n System Prompt
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! 👋 What's your name?"}
    ]

# 2. Initialize Unique Chat ID for n8n Memory
if 'chat_id' not in st.session_state:
    # FIX: Use a robust UUID to generate a unique ID, ensuring it's only done once.
    st.session_state['chat_id'] = str(uuid.uuid4())
    st.info(f"Session ID (for n8n memory): {st.session_state['chat_id'][:8]}...") 


# ==============================================================================
# N8N COMMUNICATION FUNCTION
# ==============================================================================

def get_n8n_response(prompt: str):
    """Sends the user's message to the n8n webhook with the session ID."""
    try:
        # Construct the payload required by the n8n Chat Trigger node
        payload = {
            "content": prompt,
            "chatId": st.session_state.chat_id 
        }
        
        # Send the request to the public webhook URL
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=90)
        response.raise_for_status() # Raise exception for 4xx/5xx status codes
        
        # Extract the response body (n8n Chat Trigger returns the final text)
        try:
            # Try to load as JSON first
            response_json = response.json()
            if isinstance(response_json, dict) and 'message' in response_json:
                 return response_json['message']
            # If it's not the expected dict format, fall back to string
            else:
                 return str(response.content, 'utf-8')
        except json.JSONDecodeError:
            # Handle case where n8n returns simple plain text response
            return str(response.content, 'utf-8')

    except requests.exceptions.Timeout:
        return "⚠️ The chatbot took too long to respond. Please try again or rephrase your question."
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Connection Error: Ensure your n8n and ngrok tunnels are running. Details: {e}")
        return f"🚨 Could not connect to the n8n backend. Please check your terminal windows."

# ==============================================================================
# CHAT INTERFACE LOGIC
# ==============================================================================

# 1. Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Handle user input
if prompt := st.chat_input("Ask about products, policies, or suggest a size..."):
    # Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the AI Agent's response from n8n
    with st.chat_message("assistant"):
        with st.spinner("Concierge is consulting the knowledge base..."):
            ai_response = get_n8n_response(prompt)
            st.markdown(ai_response)

    # Store AI message
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

