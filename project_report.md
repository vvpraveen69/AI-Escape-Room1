# AI-Powered Escape Room — Project Report

## 1. Introduction and Objective
This project implements an interactive escape-room game using a Large Language Model as a Game Master. The player wakes inside the Midnight Library and must investigate objects, discover clues, solve a drawer combination puzzle, collect a key and unlock the exit. The objective is to demonstrate how generative AI can create an engaging natural-language game while deterministic application logic can improve reliability and safety.

## 2. Version 1: Interactive AI Escape Room
Version 1 uses a Streamlit chat interface connected to the Google Gemini API. The player enters natural-language actions and Gemini responds as the Game Master. The application maintains the conversation history within the Streamlit session. The room includes a desk, bookshelf, painting, globe, locked drawer and exit door. The player discovers the drawer combination (314), opens the drawer to obtain a brass key, and then uses the final clue sequence (4826) to escape.

Version 1 is a baseline implementation. Most game interpretation is delegated to the LLM, so responses can be inconsistent. An LLM may misunderstand an action, accept a player's unsupported claim, invent a state change or reveal information too early. The assignment brief states that Version 1 may assume normal good-faith player behaviour, so adversarial protection is addressed in Version 2.

## 3. Version 2: Reliable AI Escape Room
Version 2 separates game rules from generated language. Python stores the authoritative state, including discovered clues, inventory, drawer status, door status and escape status. The action validator checks the player's request before state is updated. A locked drawer cannot open without the correct three-digit code and the bookshelf clue. The exit cannot open until the drawer is open, the brass key has been collected, all four clue locations have been inspected and the correct four-digit code is entered.

Gemini is used only as a narrative layer. It receives the validated outcome and is instructed not to invent state changes. If the API is unavailable, the application displays the deterministic Python response. This reduces the risk that an LLM response will corrupt the game state.

## 4. Testing and Results
The Version 2 test suite covers eight scenarios: using an uncollected key, entering an incorrect drawer code, falsely claiming a puzzle is solved, impersonating an administrator, prompt injection, attempting to escape too early, completing the valid escape sequence and examining a nonexistent object. Automated tests are provided in `version2/test_game_logic.py`. The expected behaviour is that invalid actions do not change the authoritative state, while the valid sequence successfully sets the escape flag.

Before final submission, run the tests and paste the actual test output here. Also capture screenshots of both versions, clue discovery, drawer unlocking, rejection of an invalid action and successful escape.

## 5. Limitations and Conclusion
The game state is stored in Streamlit session state and is not persisted in a database; restarting the game resets progress. The quality and style of Gemini narration can vary, and an API key and network connection are needed for generated responses. Nevertheless, the Version 2 fallback keeps core gameplay available when Gemini cannot be reached. The project demonstrates the difference between using an LLM as the sole decision-maker and using an LLM within a controlled application architecture. Python enforces the rules, while generative AI improves the player experience.
