"""
Game Glitch Investigator - Streamlit UI.

This file only handles the user interface. All game logic lives in
logic_utils.py, which is tested by tests/test_game_logic.py.
"""

import streamlit as st

from logic_utils import (
    check_guess,
    generate_secret,
    get_range_for_difficulty,
    parse_guess,
    update_score,
    update_session_stats,
    win_rate,
)

# ------------------------------------------------------------------
# Page setup
# ------------------------------------------------------------------
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

# ------------------------------------------------------------------
# Sidebar settings
# ------------------------------------------------------------------
st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# ------------------------------------------------------------------
# Session state initialization
# ------------------------------------------------------------------
if "stats" not in st.session_state:
    st.session_state.stats = {
        "games_played": 0,
        "games_won": 0,
        "best_score": 0,
    }

if "secret" not in st.session_state:
    st.session_state.secret = generate_secret(difficulty)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------------------------------------------------
# Main game area
# ------------------------------------------------------------------
st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# ------------------------------------------------------------------
# New game handler
# ------------------------------------------------------------------
if new_game:
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.secret = generate_secret(difficulty)
    st.success("New game started.")
    st.rerun()

# ------------------------------------------------------------------
# Block play if game is already over
# ------------------------------------------------------------------
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

# ------------------------------------------------------------------
# Submit handler
# ------------------------------------------------------------------
if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        outcome = check_guess(guess_int, st.session_state.secret)

        if show_hint and outcome != "Win":
            if outcome == "Too High":
                st.warning("📉 Go LOWER!")
            elif outcome == "Too Low":
                st.warning("📈 Go HIGHER!")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            update_session_stats(
                st.session_state.stats, "Win", st.session_state.score
            )
            st.success(
                f"🎉 Correct! You won! The secret was "
                f"{st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                update_session_stats(
                    st.session_state.stats, "Loss", st.session_state.score
                )
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# ------------------------------------------------------------------
# Challenge 2: Session Stats sidebar
#
# IMPORTANT: This block is at the END of the script on purpose.
# Streamlit renders top-to-bottom, so if the metrics were rendered
# before the submit handler, they would show stale values on the
# same rerun the game is won/lost. Placing them here ensures they
# pick up the freshly updated session_state.stats.
# ------------------------------------------------------------------
st.sidebar.divider()
st.sidebar.header("📊 Session Stats")

stats = st.session_state.stats
st.sidebar.metric("Games played", stats["games_played"])
st.sidebar.metric("Games won", stats["games_won"])
st.sidebar.metric("Win rate", f"{win_rate(stats)}%")
st.sidebar.metric("Best score", stats["best_score"])

if st.sidebar.button("Reset stats"):
    st.session_state.stats = {
        "games_played": 0,
        "games_won": 0,
        "best_score": 0,
    }
    st.rerun()

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.divider()
st.caption("Built by an AI that claims this code is production-ready.")