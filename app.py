import streamlit as st

from agent import Agent

st.set_page_config(page_title="Market Researcher Agent", page_icon="🤖")
st.title("🤖 AI Market Researcher")
st.caption("I can search the web and perform calculations.")

# STEP 1: INITIALIZE THE AGENT (Only once)
if "agent" not in st.session_state:
    st.session_state.agent = Agent()
    st.session_state.messages = []  # To store the conversation history

# CHECK AGENT HEALTH
if not st.session_state.agent.is_active:
    st.error(
        "⚠️ System Overload: The AI Service is currently unavailable (API Quota Exceeded). Please try again in a few minutes."
    )
    st.stop()  # stop the app from running further

# STEP 2: DISPLAY HISTORY
# We loop through the "messages" list and print them on screen
for msg in st.session_state.messages:
    # msg is a dict: {'role': 'user'/'agent', 'content': '...'}
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# STEP 3: LISTEN FOR INPUT
# st.chat_input creates a text box at the bottom
if prompt := st.chat_input("Ask me anything (e.g., 'Stock price of Tesla?')"):
    # A. Display User Message Immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # B. Add to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # C. Get Agent Response
    # We use a spinner to show it's "thinking"
    with st.chat_message("assistant"):
        with st.spinner("Thinking... (I might search the web)"):
            response = st.session_state.agent.ask(prompt)
            st.markdown(response)

    # D. Add Agent response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
