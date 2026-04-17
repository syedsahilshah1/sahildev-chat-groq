import streamlit as st
from groq import Groq

# Page Styling
st.set_page_config(page_title="Sahildev AI", page_icon="🤖", layout="wide")

# Sidebar Branding
with st.sidebar:
    st.title("👨‍💻 Sahildev AI")
    st.markdown("---")
    st.info("Powered by **Groq LPU** for ultra-fast inference.")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("💬 Sahildev ChatGPT")

# Initialize Groq using Streamlit Secrets
# This replaces the hardcoded gsk_... key
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("Please add your 'GROQ_API_KEY' to Streamlit Secrets!")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("What is on your mind?"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Sahildev is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {e}")
