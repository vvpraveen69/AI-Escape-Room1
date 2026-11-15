"""Version 2: Python-controlled escape room with Gemini narration."""
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from game_logic import new_state, process_action
from ai_game_master import narrate

st.set_page_config(page_title="The Midnight Library - V2", page_icon="🔐", layout="wide")
st.title("🔐 The Midnight Library")
st.caption("Version 2 | Python-controlled game logic | Gemini-powered narration")

if "game_state" not in st.session_state:
    st.session_state.game_state = new_state()
if "chat" not in st.session_state:
    st.session_state.chat = [{"role": "assistant", "content": (
        "Welcome to the Midnight Library! You are locked inside. Explore "
        "the desk, bookshelf, painting and globe. Discover the clues, open "
        "the locked drawer, collect the brass key and find your way out. "
        "Your actions are validated by the Python game engine."
    )}]

with st.sidebar:
    st.header("📋 Game Status")
    state = st.session_state.game_state
    st.write("**Clues discovered:**", f"{len(state['inspected'])}/4")
    st.write("**Inventory:**", ", ".join(state["inventory"]) if state["inventory"] else "Empty")
    st.write("**Drawer:**", "Open" if state["drawer_open"] else "Locked")
    st.write("**Exit:**", "Escaped" if state["escaped"] else "Locked")
    with st.expander("📖 Instructions and Help"):
        st.write("Inspect the four room objects, solve the drawer puzzle, collect the key and unlock the exit.")
        st.markdown("- `examine desk`\n- `examine bookshelf`\n- `examine painting`\n- `examine globe`\n- `inspect drawer`\n- `inventory`\n- `help`")
    if st.button("🔄 Restart Game", use_container_width=True):
        st.session_state.game_state = new_state()
        st.session_state.chat = [{"role": "assistant", "content": "The library resets. Rain taps against the windows. What will you investigate first?"}]
        st.rerun()

left, right = st.columns([2, 1])
with right:
    st.subheader("🏛️ Room Objects")
    st.markdown("- 🗃️ Desk\n- 📚 Bookshelf\n- 🖼️ Painting\n- 🌍 Globe\n- 🔒 Locked Drawer\n- 🚪 Exit Door")
    st.info("Version 2 security: Python validates every action and controls inventory, puzzle progress and escape status. Gemini is used only for narration.")
with left:
    st.subheader("💬 Game Master")
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("Describe your action...", disabled=st.session_state.game_state["escaped"])
if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})
    validated_result = process_action(prompt, st.session_state.game_state)
    response_text = narrate(prompt, validated_result, st.session_state.game_state)
    st.session_state.chat.append({"role": "assistant", "content": response_text})
    st.rerun()

if st.session_state.game_state["escaped"]:
    st.success("🎉 Congratulations! You escaped the Midnight Library!")
    st.balloons()
