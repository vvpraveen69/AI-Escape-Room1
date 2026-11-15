"""Version 1: conversational AI Escape Room. The LLM is the primary game master."""
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """You are the Game Master of 'The Midnight Library', a friendly but mysterious escape-room game.
The player wakes in a locked library. The room contains a desk, bookshelf, painting, globe, locked drawer and exit door.
Respond vividly and helpfully to natural-language actions. Keep the story coherent and remember the conversation supplied.
There are three puzzle stages: discover clues around the room; open the drawer using the three-digit code 314; then use the four-digit exit code 4826.
Clue hints: desk has four candle marks; bookshelf has eight gold-spined books and three marked books numbered 3, 1, 4; painting has two moons; globe has six red pins.
The drawer contains a brass key and a note explaining that the final code is formed by the desk, bookshelf, painting and globe clues in that order: 4826.
Do not reveal solutions unless the player has reasonably discovered the clues or explicitly asks for a hint. For this Version 1, assume normal good-faith play; do not implement security enforcement.
Keep replies concise (2-5 sentences), immersive, and tell the player what they can try next. Never claim the player has escaped unless they correctly enter 4826 after opening the drawer."""

st.set_page_config(page_title="The Midnight Library — V1", page_icon="🗝️", layout="wide")
st.title("🗝️ The Midnight Library")
st.caption("Version 1 · Interactive AI Escape Room · Gemini as Game Master")
with st.sidebar:
    st.header("How to play")
    st.write("Explore the library using natural language. Try: *examine the desk*, *inspect the bookshelf*, *open the drawer with 314*, or *unlock the door with 4826*.")
    st.info("Your goal: discover clues, open the drawer, find the key and escape.")
    if st.button("🔄 Restart game", use_container_width=True):
        st.session_state.messages = []
        st.session_state.escaped = False
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "You awaken in the Midnight Library. Rain taps against tall windows. A desk, bookshelf, painting, globe, locked drawer and a heavy exit door surround you. The door has a four-digit keypad. What would you like to do first?"}]
if "escaped" not in st.session_state:
    st.session_state.escaped = False

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.warning("Gemini API key not found. Add GEMINI_API_KEY to a local .env file. The opening scene is available, but AI replies require the key.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What do you want to do in the library?", disabled=st.session_state.escaped)
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    reply = "I cannot reach the Game Master right now. Check your GEMINI_API_KEY and internet connection, then try again."
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            history = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages[-16:])
            response = client.models.generate_content(
                model=MODEL,
                contents=f"{SYSTEM_PROMPT}\n\nConversation so far:\n{history}\n\nRespond to the latest player action.",
            )
            if response.text:
                reply = response.text.strip()
        except Exception as exc:
            reply = f"The Game Master is temporarily unavailable. Check the API key, model name and network connection. (Technical detail: {type(exc).__name__})"
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
