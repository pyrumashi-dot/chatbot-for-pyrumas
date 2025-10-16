import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. STREAMLIT APPLICATION SETUP
# ==============================================================================

st.set_page_config(
    page_title="Embedded n8n Concierge",
    layout="wide"
)

# Optional: Add a brief Streamlit header outside the embedded chat
st.header("Seamless Chatbot Integration via n8n Widget")
st.markdown("""
This page uses Streamlit to host the official n8n Chat Widget. 
The entire conversation logic (AI, Memory, Google Sheets) runs on your n8n instance.
""")

# ==============================================================================
# 2. EMBEDDED HTML CONTENT (FROM index.html)
# ==============================================================================

# Note: The entire HTML file contents (CSS, structure, and JavaScript initialization) 
# are stored here as a raw string.
# The URL inside is the LIVE NGROK URL: https://libbie-semidramatic-cesar.ngrok-free.dev/...
HTML_WIDGET_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Embedded Chat</title>
    <!-- 1. Load the n8n Chat Widget styles -->
    <link href="https://cdn.jsdelivr.net/npm/@n8n/chat/dist/style.css" rel="stylesheet" />
    <style>
        /* Styling for the container within the Streamlit frame */
        body {
            font-family: sans-serif;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }
        #n8n-chat-container {
            height: 800px; /* Give the chat container a fixed height */
            width: 100%;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }
    </style>
</head>
<body>

    <!-- Chat container: Given fixed height in CSS above -->
    <div id="n8n-chat-container"></div>

    <!-- 3. Load the n8n Chat Widget script and initialize it -->
    <script type="module">
        import { createChat } from 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/chat.bundle.es.js';

        // 🚨 LIVE URL: Uses the ngrok tunnel endpoint
        const LIVE_WEBHOOK_URL = 'https://libbie-semidramatic-cesar.ngrok-free.dev/webhook/970120ca-bb27-4bcd-805f-87f4a331b2a1/chat';

        createChat({
            webhookUrl: LIVE_WEBHOOK_URL,
            containerId: 'n8n-chat-container', 
            title: "Concierge Bot (Live)",
            subtitle: "Ask me anything about our products.",
            placeholderText: "Type your name or question..."
        });
    </script>

</body>
</html>
"""

# ==============================================================================
# 3. RENDER THE WIDGET
# ==============================================================================

# Render the HTML content inside the Streamlit app
components.html(
    HTML_WIDGET_CODE,
    height=820, # Set the height of the entire Streamlit component frame
    scrolling=False
)

