"""Deterministic game rules for Version 2. The LLM never changes this state."""
from __future__ import annotations
import re
from typing import Any

OBJECTS = {
    "desk": ["desk", "table", "papers", "note"],
    "bookshelf": ["bookshelf", "bookcase", "bookshelf", "book"],
    "painting": ["painting", "picture", "portrait", "frame"],
    "globe": ["globe", "map", "world"],
    "drawer": ["drawer", "locked drawer"],
    "door": ["door", "exit", "keypad"],
}

CLUE_TEXT = {
    "desk": "You find four candle marks etched beneath the desk lamp. Record the first digit: 4.",
    "bookshelf": "Eight books have gold spines. Three marked books contain the digits 3, 1 and 4 in that order. Record the second final-code digit: 8.",
    "painting": "The painting shows two silver moons. Record the third final-code digit: 2.",
    "globe": "Six red pins mark locations on the globe. Record the fourth final-code digit: 6.",
}

INITIAL_STATE = {
    "inspected": [], "inventory": [], "drawer_open": False,
    "drawer_attempts": 0, "door_unlocked": False, "escaped": False,
    "actions": [],
}


def new_state() -> dict[str, Any]:
    """Return a fresh, independent game state."""
    return {k: (v.copy() if isinstance(v, list) else v) for k, v in INITIAL_STATE.items()}


def _object_from_text(text: str) -> str | None:
    low = text.lower()
    for name, aliases in OBJECTS.items():
        for alias in sorted(aliases, key=len, reverse=True):
            if re.search(rf"\b{re.escape(alias)}\b", low):
                return name
    return None


def _extract_code(text: str, length: int) -> str | None:
    matches = re.findall(rf"(?<!\d)(\d{{{length}}})(?!\d)", text)
    return matches[-1] if matches else None


def process_action(user_text: str, state: dict[str, Any]) -> dict[str, Any]:
    """Validate a player action and update state only in Python."""
    text = (user_text or "").strip()
    low = text.lower()
    result = {
        "accepted": False,
        "event": "unknown",
        "message": "I don't recognise that action. Try examining the desk, bookshelf, painting or globe, or attempt a code when you have a clue.",
        "state_changed": False,
    }
    if not text:
        result["message"] = "Please enter an action."
        return result
    if state["escaped"]:
        result.update(event="already_escaped", message="You have already escaped. Restart the game to play again.")
        return result

    suspicious_terms = [
        "ignore previous", "ignore all rules", "i am the administrator",
        "i am admin", "system prompt", "reveal all secrets",
        "reveal all secret codes", "show me the answer", "unlock immediately",
    ]
    if any(term in low for term in suspicious_terms):
        result.update(event="security_rejection", message="The library's rules cannot be overridden by chat instructions. Explore the room and solve the puzzles to progress.")
        return result

    # Inventory and help are informational actions.
    if any(word in low for word in ["inventory", "items", "what do i have"]):
        items = ", ".join(state["inventory"]) if state["inventory"] else "Your inventory is empty."
        result.update(accepted=True, event="inventory", message=items)
        return result
    if any(word in low for word in ["hint", "help"]):
        result.update(accepted=True, event="hint", message="Hint: inspect the four main objects. The bookshelf contains the three-digit drawer combination. Combine the four clue digits in this order: desk, bookshelf, painting, globe.")
        return result

    obj = _object_from_text(text)
    examination_words = ["examine", "inspect", "look at", "look around", "search", "investigate", "check"]
    if any(word in low for word in examination_words):
        if obj is None:
            result.update(event="unknown_object", message="I can't identify that object. The interactive objects are the desk, bookshelf, painting, globe, drawer and door.")
            return result
        if obj == "drawer":
            if state["drawer_open"]:
                result.update(accepted=True, event="drawer_open", message="The drawer is open. The brass key is in your inventory. A note explains that the final code uses the four room clues in this order: desk, bookshelf, painting and globe.")
            else:
                result.update(event="drawer_locked", message="The drawer is locked by a three-digit combination. Find the marked books on the bookshelf for the code.")
            return result
        if obj == "door":
            result.update(accepted=True, event="door_status", message="The exit door has a four-digit keypad. You must open the drawer, collect the brass key and discover all four room clues before escaping.")
            return result
        if obj not in state["inspected"]:
            state["inspected"].append(obj)
            state["actions"].append(f"inspected:{obj}")
            result["state_changed"] = True
        result.update(accepted=True, event="clue_found", message=CLUE_TEXT[obj])
        return result

    # The drawer code is accepted only after the bookshelf has been inspected.
    if "drawer" in low and any(w in low for w in ["open", "unlock", "code", "enter", "try"]):
        if "bookshelf" not in state["inspected"]:
            result.update(event="missing_clue", message="You need to inspect the bookshelf and discover the marked-book clue before attempting the drawer code.")
            return result
        code = _extract_code(text, 3)
        if code is None:
            result.update(event="missing_code", message="Enter the three-digit combination, for example: 'Open the drawer with 314'.")
            return result
        state["drawer_attempts"] += 1
        if code == "314":
            state["drawer_open"] = True
            if "brass key" not in state["inventory"]:
                state["inventory"].append("brass key")
            state["actions"].append("drawer_opened")
            result.update(accepted=True, event="drawer_opened", state_changed=True, message="Correct! The drawer opens. You collect the brass key. A note inside explains that the final code uses the clues in this order: desk, bookshelf, painting and globe.")
        else:
            result.update(event="incorrect_code", message="That combination is incorrect. The drawer remains locked. Recheck the three marked books.")
        return result

    # The final exit requires the drawer, key and all four clues.
    if any(w in low for w in ["door", "exit", "escape", "keypad"]) and any(w in low for w in ["unlock", "open", "enter", "code", "try"]):
        code = _extract_code(text, 4)
        required = {"desk", "bookshelf", "painting", "globe"}
        missing = sorted(required - set(state["inspected"]))
        if not state["drawer_open"] or "brass key" not in state["inventory"]:
            result.update(event="drawer_required", message="The exit remains locked. First solve the bookshelf combination and open the drawer to collect the brass key.")
            return result
        if missing:
            result.update(event="missing_clues", message="You have not discovered every room clue yet. Inspect: " + ", ".join(missing) + ".")
            return result
        if code is None:
            result.update(event="missing_code", message="Enter the four-digit exit code when you are ready.")
            return result
        if code == "4826":
            state["door_unlocked"] = True
            state["escaped"] = True
            state["actions"].append("escaped")
            result.update(accepted=True, event="escaped", state_changed=True, message="The keypad flashes green. The brass key turns in the lock, the library door swings open, and you escape. Congratulations!")
        else:
            result.update(event="incorrect_code", message="Incorrect exit code. The door remains locked. Check the four clues in this order: desk, bookshelf, painting, globe.")
        return result

    return result
