# AI-Powered Escape Room — The Midnight Library

An interactive escape-room mini-project built with Python, Streamlit and Google Gemini. The repository contains two implementations: an LLM-led baseline (Version 1) and a deterministic Python-controlled implementation (Version 2).

## Project objective
The player is locked inside a midnight library and must inspect objects, discover four clues, solve a three-digit drawer puzzle, collect a brass key and enter the final exit code.

## Versions

### Version 1 — LLM-led baseline
- Streamlit chat interface with Gemini acting as Game Master.
- Maintains conversation history during the session.
- Includes a library setting, interactive objects and escape challenge.
- Designed as the baseline; game outcomes rely more heavily on model responses and are less robust against adversarial input.

### Version 2 — Deterministic Python game engine
- Python owns the authoritative game state: inspected clues, inventory, drawer, door and escape status.
- Python validates actions and codes before the response is narrated.
- Gemini is used only for optional atmospheric narration; if the API is unavailable, Python's validated message is shown.
- Rejects invalid objects, incorrect codes, premature escape attempts and common prompt-injection phrases.
- Includes automated unit tests in `version2/test_game_logic.py`.

## Technology stack
- Python 3.10+
- Streamlit
- Google Gemini API (`google-genai`)
- `python-dotenv`
- Python `unittest`

## Repository structure

```text
AI-Escape-Room/
├── version1/                  # Version 1 Streamlit application
├── version2/                  # Version 2 application, game engine and tests
├── tests/                     # Additional test material
├── docs/                      # Architecture, test plan and screenshots
├── report/                    # Project report (PDF and editable Markdown)
├── .env.example               # Environment-variable template (no real key)
├── .gitignore                 # Excludes secrets and local environments
├── requirements.txt
└── README.md
```

## Setup

1. Install Python 3.10 or newer.
2. Open a terminal in the repository root.
3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate it (Windows PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, you can use `.venv\Scripts\python.exe` directly for the commands below.

5. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Copy `.env.example` to `.env` and put your own Gemini API key in `.env`. **Never upload `.env` or share your API key.**

## Run the applications

From the repository root:

```bash
streamlit run version1/app.py
```

For Version 2, open another terminal in the repository root and run:

```bash
streamlit run version2/app.py
```

If you do not configure a Gemini API key, Version 2 still runs using the deterministic Python response text; Gemini narration is simply disabled.

## How to play

1. Inspect the desk, bookshelf, painting and globe.
2. The bookshelf clue gives the drawer combination.
3. Enter `open drawer with 314` after inspecting the bookshelf.
4. Collect the brass key.
5. Combine the four clue digits in this order: desk, bookshelf, painting, globe.
6. Enter `unlock door with 4826` after all clues are found and the drawer is open.

Other supported actions include `inventory`, `hint`, `help` and `inspect drawer`.

## Run automated tests

From the repository root:

```bash
python -m unittest version2.test_game_logic -v
```

The tests cover initial state, clue discovery, unknown objects, missing prerequisites, incorrect drawer codes, key collection, exit requirements, prompt injection rejection, successful escape and actions after escape. The checked-in test suite contains 10 tests.

## Architecture and test evidence

- Version 1 and Version 2 diagrams: `docs/architecture_v1.png` and `docs/architecture_v2.png`.
- Architecture explanation: `docs/architecture.md`.
- Manual test scenarios: `docs/test_cases.md`.
- Screenshots: `docs/screenshots/`.
- Project report: `report/AI_Escape_Room_Project_Report.pdf` and `report/project_report.md`.

## Security notes and limitations
- The API key is read from the `GEMINI_API_KEY` environment variable.
- `.env` is excluded through `.gitignore`; commit `.env.example` only.
- Version 2 state is held in Streamlit session state and is reset when the game is restarted; it is not stored in a persistent database.
- Prompt-injection phrase checks are a basic demonstration, not a complete general-purpose security filter. The main protection is that the LLM is not given authority to modify game state and Python validates all state transitions.
- Gemini availability and response quality depend on the configured model and network access.

## Development history
Use meaningful commits as you upload and maintain the project. Do not invent historical commits. Suggested commit messages include `feat: add V1 Streamlit escape room`, `feat: add deterministic V2 game engine`, `test: add gameplay and adversarial tests`, and `docs: add diagrams and project report`.
