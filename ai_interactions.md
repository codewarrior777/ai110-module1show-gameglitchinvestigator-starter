# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

```
Add a "Session Stats" sidebar to the Game Glitch Investigator app that tracks
cumulative statistics across multiple rounds. The sidebar should display:
- Games played
- Games won
- Win rate (as a percentage)
- Best score

Requirements:
1. Store the stats in st.session_state so they persist across Streamlit reruns.
2. Add two pure functions to logic_utils.py: update_session_stats(stats, outcome, score)
   and win_rate(stats) — keep the logic separate from the UI for testability.
3. Update the stats every time a game ends (win or loss).
4. Include a "Reset stats" button in the sidebar.
5. Follow the existing code style (comments in English, PEP 8).
```

**What did the agent do?**

Files edited:
- `logic_utils.py` — Added `update_session_stats()` and `win_rate()` at the end of the file. Both functions are pure (no Streamlit imports) so they can be unit tested.
- `app.py` —
  - Added imports for the two new functions.
  - Initialized `st.session_state.stats` with default keys (`games_played`, `games_won`, `best_score`).
  - Added a "📊 Session Stats" sidebar section with `st.metric()` calls and a "Reset stats" button.
  - Called `update_session_stats()` inside the win branch and the loss branch of the submit handler.

**What did you have to verify or fix manually?**

The AI's first version placed the sidebar metrics **before** the submit handler. This caused a bug: when the player won, the sidebar displayed **stale values** (0 games played, 0 games won) because Streamlit renders top-to-bottom in a single pass.

I fixed it by:
1. Moving the entire "Session Stats" sidebar block **to the end of the script**, after the submit handler. This way, on the same rerun the game is won, the metrics render with the freshly updated values.
2. Adding an inline comment explaining **why** the block is at the bottom, so a future reader doesn't "helpfully" move it back and re-introduce the bug.

I also discovered a separate mismatch: my first `update_session_stats()` incremented `games_played` only on "New Game" outcomes. After integrating the UI, `games_played` stayed at 0 while `games_won` went to 1. I fixed the function so it increments `games_played` **every time the function is called** (Win or Loss), and only `games_won` is conditional.

**Verification:**

- Played one winning round → sidebar showed: Games played: 1, Games won: 1, Win rate: 100.0%, Best score: 90.
- Played one losing round → sidebar showed: Games played: 2, Games won: 1, Win rate: 50.0%, Best score: 90.
- Clicked "Reset stats" → all metrics returned to 0.
- Ran `python -m pytest tests/ -v` → all 6 tests still pass.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used (verbatim):**

```
I need 3 pytest edge case tests for a function called parse_guess that
converts user input strings into integers. The function returns a tuple:
(ok: bool, value: int | None, error_message: str | None).

Test these three edge cases:
1. Non-numeric input like "abc"
2. Empty string ""
3. Decimal written as string like "3.7"

For each, show the assertion that proves the correct behavior.
```

**AI-suggested tests table:**

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| `"abc"` (non-numeric) | Above prompt | `test_parse_guess_rejects_non_numeric_input` | ✅ Yes | Users can type letters by accident. The parser must reject without crashing and return a helpful error message. |
| `""` (empty string) | Above prompt | `test_parse_guess_rejects_empty_input` | ✅ Yes | If the user clicks Submit without typing anything, the game should not crash — it should prompt them to enter a guess. |
| `"3.7"` (decimal as string) | Above prompt | `test_parse_guess_converts_float_string_to_int` | ✅ Yes | The original parser explicitly handles this case via `int(float(raw))`. Locking the behavior with a test prevents future regressions. |

**Verification:**

All 6 tests (3 core + 3 edge case) pass:

```
$ python -m pytest tests/ -v
============================= test session starts =============================
collected 6 items

tests/test_game_logic.py::test_winning_guess PASSED                       [ 16%]
tests/test_game_logic.py::test_guess_too_high PASSED                      [ 33%]
tests/test_game_logic.py::test_guess_too_low PASSED                       [ 50%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_input PASSED  [ 66%]
tests/test_game_logic.py::test_parse_guess_rejects_empty_input PASSED     [ 83%]
tests/test_game_logic.py::test_parse_guess_converts_float_string_to_int PASSED [100%]

============================== 6 passed in 0.41s ==============================
```

**Notes on AI suggestions:**

- The AI proposed all three edge cases when prompted.
- It also proposed a 4th test for negative numbers (`"-5"`), which I rejected: negative guesses are out of scope for a game where the range is 1–100. Adding that test would suggest negative input is expected, which is misleading.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Install ruff in my virtual environment and run it against logic_utils.py and
app.py. For each warning it reports:
1. Explain in plain English what the warning means.
2. Show the before/after of the suggested fix.
3. Confirm the fix keeps the existing behavior.
Then apply the fix and re-run ruff to confirm the code is clean.
```

**Linting output before:**

```
$ ruff check logic_utils.py app.py
PLR1730 [*] Replace `if` statement with `max` call
  --> logic_utils.py:108:9
   |
106 |     if outcome == "Win":
107 |         stats["games_won"] += 1
108 |         if score > stats["best_score"]:
109 |             stats["best_score"] = score
   |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
110 |
   |
help: Replace with `max` call

Found 1 error.
[*] 1 fixable with the `--fix` option.
```

**Changes applied:**

The linter flagged one stylistic improvement in `update_session_stats()`. The original code used an explicit `if` comparison to update `best_score`:

```python
# Before
if score > stats["best_score"]:
    stats["best_score"] = score
```

`ruff` suggested replacing it with Python's built-in `max()`:

```python
# After
stats["best_score"] = max(stats["best_score"], score)
```

**Why I applied it:**
- It's more idiomatic Python — `max()` clearly expresses the intent ("keep the larger of these two values").
- It's shorter (1 line vs 2) and eliminates a branch.
- Behavior is identical; I verified by running the test suite and manually playing both a winning and a losing round.

**Verification:**

```
$ ruff check logic_utils.py app.py
All checks passed!

$ python -m pytest tests/ -v
============================== 6 passed in 0.63s ==============================
```

**Notes on what I did NOT apply:**

`ruff` did not report any other warnings in either file, so no other changes were needed. I checked manually that `logic_utils.py` already had PEP 257-style docstrings on every function before the linting step, so no additional documentation was required for this challenge.

---

## UI Enhancements (Challenge 4)

> Document the UI improvements added to the game.

**Features added:**

1. **Progress bar** — Replaced the plain-text attempt counter with `st.progress()` showing a visual bar of attempts used vs allowed.
2. **Color-coded hints** — Wrong guesses now render as `st.error()` (red) for "Too High" and `st.info()` (blue) for "Too Low", making the direction obvious at a glance. Each hint also includes a short parenthetical explanation.
3. **Hot/Cold thermometer** — Each guess is scored on proximity to the secret using `proximity_emoji()` and `proximity_label()` in `logic_utils.py`. Results range from `🔥🔥🔥 Very close!` (diff ≤ 5) to `❄️ Cold` (diff > 30).
4. **Attempt history table** — All attempts are logged as dicts and rendered with `st.dataframe()`, showing attempt number, guess, result, heat, and score delta in one view.

**Files modified:**
- `logic_utils.py` — Added `proximity_emoji()` and `proximity_label()`. Both are pure functions (no Streamlit imports) so they could be unit tested if needed.
- `app.py` — Replaced counter with progress bar; added thermometer display after each guess; changed history storage from list-of-ints to list-of-dicts so it can be rendered as a table; added the "📋 Attempt History" section.

**Why this improves the experience:**

The original game showed a single cryptic hint and a running attempt count. The improvements:
- Make the direction hint **visually obvious** (color = immediate signal).
- Give the player a **sense of progress** with the bar.
- Communicate **how close** they are, not just the direction.
- Provide a **review screen** showing all attempts — useful for learning patterns.

**Verification:**

Tested manually:
- Guess 23 (secret 28, diff 5) → 🔥🔥🔥 "Very close!" ✅
- Guess 23 (secret 60, diff 37) → ❄️ "Cold" ✅
- Progress bar fills correctly with each attempt ✅
- Attempt History table updates after every guess ✅
- All 6 pytest tests still pass ✅

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

```
I have this buggy Python function:

def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"
    try:
        if guess > secret:
            return "Too High", "📈 Go HIGHER!"
        else:
            return "Too Low", "📉 Go LOWER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📈 Go HIGHER!"
        return "Too Low", "📉 Go LOWER!"

The bug: when guess > secret, the player is told "Go HIGHER!" but they
should be told "Go LOWER!" because their guess was too high. The same
inversion exists for the other branch.

Fix the bug and explain your reasoning.
```

| | Model A | Model B |
|-|---------|---------|
| **Model name** | ChatGPT (GPT-4o) | Gemini (Flash) |
| **Response summary** | Fixed both branches by swapping the hint strings, plus the TypeError fallback. Explained each branch in short bullet points. | Fixed both branches by swapping the hint strings, plus the TypeError fallback. Explained each branch with numbered subsections ("Branch 1", "Branch 2", "TypeError Block"). |
| **More Pythonic?** | Tie — both produced the same fix, keeping the original `try/except` structure. | Tie — same fix. |
| **Clearer explanation?** | **ChatGPT** — the bullets were short and scannable. | **Gemini** — the numbered structure was more thorough but longer. |

**Which did you prefer and why?**

I preferred **ChatGPT's response** for this specific bug. The bug is small (one line per branch), so a verbose explanation was overkill. ChatGPT's three bullets — "guess > secret means the player should go LOWER", "guess < secret means the player should go HIGHER", "the TypeError fallback has the same inversion" — explained everything in ~15 seconds of reading.

Gemini's response was more thorough and would have been better for a **larger, more complex refactor**. For a two-line fix, it was more text than necessary. Both models are equally correct; the choice comes down to **explanation density vs. explanation depth**.

**Observation neither model made:**

Neither model pointed out that the `try/except TypeError` block is **dead code** in Python 3. Comparing an `int` to a `str` with `>` raises a `TypeError`, but the outer logic already ensures `guess` and `secret` are both integers when this function is called. Removing the `try/except` entirely would be a more "Pythonic" fix, but it would also change behavior if the function is ever called with mixed types. I kept the fix minimal to avoid introducing regressions.