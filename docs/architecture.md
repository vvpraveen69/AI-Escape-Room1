# System Architecture

## Version 1 — Conversational AI Game Master

```mermaid
flowchart TD
    A[Player] --> B[Streamlit Chat Interface]
    B --> C[Python Application]
    C --> D[Conversation History]
    C --> E[Gemini API]
    E --> F[Generated Game Master Response]
    F --> B
```

The player sends natural-language messages through Streamlit. The Python application includes the conversation history and game instructions in a Gemini request. Gemini generates the Game Master's reply. Version 1 is a baseline and assumes normal good-faith play.

## Version 2 — Python-Controlled Reliable Game

```mermaid
flowchart TD
    A[Player] --> B[Streamlit Interface]
    B --> C[Python Game Controller]
    C --> D[Action Validator]
    D --> E[Authoritative Game State]
    E --> F[Puzzle and Inventory Rules]
    F --> G{Action Valid?}
    G -->|Yes| H[Update State in Python]
    G -->|No| I[Reject Action]
    H --> J[Validated Result]
    I --> J
    J --> K[Gemini Narrative Layer]
    K --> L[Display Response]
    L --> B
```

Python validates all actions and owns the game state. Gemini receives the already validated result and may only narrate it. If Gemini is unavailable, Python's validated message is displayed.
