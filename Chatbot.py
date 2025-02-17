import openai
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables securely
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to display chat messages
def show_messages(text):
    """Displays chat history in Streamlit."""
    messages_str = [
        f"<span style='color: green;'><b>USER</b>: {_['content']}</span><br>"  
        if _['role'] == 'user' 
        else f"<span style='color: white;'><b>BOT</b>: {_['content']}</span><br><br>"
        for _ in st.session_state["messages"][1:]
    ]
    text.markdown("### Chat History", unsafe_allow_html=True)
    text.markdown("\n".join(messages_str), unsafe_allow_html=True)

# Initial chatbot message
BASE_PROMPT = [
    {"role": "system", "content": """
        Hello! I'm your AI fitness assistant, here to guide you with workouts and fitness tips. 
        Let me know what type of routine you're looking for, and I’ll provide a plan.
        I can help with strength training, cardio, flexibility, and workout splits.
        Let's get started—what are your fitness goals?
    """}
]

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

# Streamlit UI
st.title("🏋️‍♂️ AI Gym Assistant")
st.write("💬 Get customized fitness advice!")

text = st.empty()  # Chat display container
show_messages(text)

# User input handling
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def submit():
    """Handles user input submission."""
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ''

# Input box
st.text_input("💡 Ask your fitness assistant:", key="widget", on_change=submit)

if st.session_state.user_input:
    with st.spinner("💭 Thinking..."):
        # Add user message
        st.session_state["messages"].append({"role": "user", "content": st.session_state.user_input})

        # Get AI-generated response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["messages"]
        )

        # Store and display bot response
        bot_reply = response["choices"][0]["message"]["content"]
        st.session_state["messages"].append({"role": "system", "content": bot_reply})
        show_messages(text)

    # Clear user input
    st.session_state.user_input = ""

# Clear button to reset chat
if st.button("🔄 Reset Chat"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
