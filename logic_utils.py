"""
Game Glitch Investigator - Core game logic.

Extracted from app.py so it can be tested independently with pytest.
"""

import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """
    Compare guess to secret and return the outcome.

    Returns one of: "Win", "Too High", "Too Low".

    FIX: This function previously returned a tuple (outcome, message)
    and had the higher/lower hints swapped. It now returns only the
    outcome, and the message is built by the caller.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Update score based on outcome and attempt number.

    FIX: Previously, guessing 'Too High' on even attempts ADDED points,
    which was confusing. Now, wrong guesses always subtract a flat
    penalty, and wins award a bonus that decreases with attempts.
    """
    if outcome == "Win":
        # Fewer attempts = bigger bonus. Minimum 10 points.
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score


def generate_secret(difficulty: str) -> int:
    """Generate a random secret within the difficulty's range."""
    low, high = get_range_for_difficulty(difficulty)
    return random.randint(low, high)