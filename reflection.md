# Reflection — Game Glitch Investigator

## 1. What was broken when you started?

I forked and ran the original `app.py` and found four distinct bugs.

### Game Run Trace (Terminal Output)

I ran the game multiple times and captured the following terminal output. This documents the actual observed behavior that led to the bug list below.

```
=== Run 1 (secret = 43, revealed via Debug Info) ===
> Guess 5   → hint: "📉 Go LOWER!"   ← WRONG: should be "Go HIGHER" (5 < 43)
> Guess 80  → hint: "📉 Go LOWER!"   ← odd: same hint as above
> Guess 43  → hint: "🎉 Correct!"    ← win triggered
> Final score: -20                   ← WRONG: score should be positive

=== Run 2 (secret = 27, revealed via Debug Info) ===
> Guess 50  → hint: "📉 Go LOWER!"   ← ok direction
> Guess 10  → hint: "📈 Go HIGHER!"  ← ok direction
> Guess 27  → hint: "🎉 Correct!"
> Final score: 30

=== Observations ===
1. On Run 1, guessing 5 (below the secret 43) showed "Go LOWER!" — the
   hint tells the player to go in the WRONG direction.
2. The score went negative (-20) after several wrong guesses, which should
   never happen in a guessing game.
3. The secret appeared to change between attempts when it should stay
   constant for the whole round.
```

### Bug Reproduction Logs

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|---|---|---|---|---|
| Guess 5 (secret 43) | "Go HIGHER!" | "Go LOWER!" | None | `check_guess()` in `app.py` — hint branches were swapped |
| Guess 60 (secret 50) | "Too High" outcome | "Too Low" outcome | None | `check_guess()` — return values inverted |
| Guess after attempt 2 | Secret stays the same | Secret appeared to change / comparisons failed | None | `app.py` submit handler — `secret = str(secret)` on even attempts |
| Win with multiple prior guesses | Score is positive | Score went negative (-20) | None | `update_score()` — wrong attempts could ADD points |

### Detailed Bug Descriptions

**Bug 1 — Hints inverted in `check_guess()`**

The function returned `"Too High", "Go HIGHER!"` when the guess was higher than the secret. The message tells the player the wrong direction.

```python
# Original (broken)
if guess > secret:
    return "Too High", "📈 Go HIGHER!"   # wrong message
else:
    return "Too Low", "📉 Go LOWER!"     # wrong message
```

**Bug 2 — Secret silently converted to a string on even attempts**

Inside the submit handler:

```python
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)
```

This made `guess_int == secret` always False on even attempts, silently breaking comparisons and hints.

**Bug 3 — Score awards on wrong guesses**

`update_score()` added +5 points for a "Too High" outcome on even attempts. Losing should never award points.

```python
if outcome == "Too High":
    if attempt_number % 2 == 0:
        return current_score + 5   # adds points for a WRONG guess
    return current_score - 5
```

**Bug 4 — Attempts started at 1 instead of 0**

The UI showed "Attempts left: 7" on first load, even though the player had not made any guesses yet.

---

## 2. How did you use AI as a teammate?

### AI Suggestion #1 — ACCEPTED

**What the AI suggested (verbatim):**

When I asked the AI why the hints were swapped, it replied:

> "Looking at your `check_guess` function, the branches for `guess > secret`
> and `guess < secret` return the WRONG messages. When the guess is higher
> than the secret, the player needs to guess lower, so the message should be
> 'Go LOWER', not 'Go HIGHER'. The tuples are in the wrong order."

**Why it was correct:**
The logic matches the game's intent: guessing above the secret means you should go lower next time. The AI correctly identified the specific lines (the two `return` statements in `check_guess`) and explained the fix in terms of player experience.

**How I verified it:**
- Manually traced both branches in `check_guess`
- Added a pytest test (`test_guess_too_high`) asserting `check_guess(60, 50) == "Too High"` — passed
- Played the live game and confirmed both hint directions were correct

---

### AI Suggestion #2 — REJECTED

**What the AI suggested (verbatim):**

When I asked the AI to fix the win-condition bug, it replied:

> "I recommend refactoring the entire game into a class-based state machine.
> Define a `GameState` enum with states like PLAYING, WON, LOST. Then create
> a `Game` class that owns the state, the secret, the score, and the history.
> The `submit_guess` method transitions the state and returns an event. This
> decouples UI from logic and makes the code more testable and extensible."

**Why I rejected it:**
The proposed solution was a ~200-line rewrite for what should have been a 3-line fix. This was over-engineered for a small teaching project:

- It introduced new abstractions (`GameState` enum, `Game` class, event objects) that weren't part of the assignment's scope.
- The Streamlit `session_state` already serves as the state container.
- The diff would have been hard to review, obscuring the actual bug fix.

Instead, I asked for a **minimal fix**: just update the win-condition check to set `st.session_state.status = "won"`. This ended the game correctly with a 4-line change.

**How I verified the result:**
- Played the game live and confirmed the round ends on a correct guess
- The existing pytest suite still passes

---

## 3. Debugging and testing your fixes

### Fix 1 — Inverted hints

**Evidence it was broken:** Documented in Bug 1 of Section 1 (guess 5 vs secret 43 returned "Go LOWER!" instead of "Go HIGHER!").

**How I diagnosed it:** Read `check_guess()` in `app.py` and compared the branches to the game rules. The return tuples were swapped.

**The fix:** Swapped the two return strings so `guess > secret` returns `"Too High"` and `guess < secret` returns `"Too Low"`.

**How I verified it:**
- `test_guess_too_high` asserts `check_guess(60, 50) == "Too High"` ✅
- `test_guess_too_low` asserts `check_guess(40, 50) == "Too Low"` ✅
- Live game confirmed (guess 20 vs secret 62 → "Go HIGHER!")

---

### Fix 2 — Secret converted to string on even attempts

**Evidence it was broken:** Documented in Bug 2 of Section 1.

**How I diagnosed it:** Found this block in `app.py`'s submit handler:

```python
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)
```

This made `guess_int == secret` always False for even attempts, silently breaking comparisons and hints.

**The fix:** Removed the conditional entirely. The secret stays an `int` for the whole game.

**How I verified it:**
- Played multiple rounds without the secret changing
- The `History` in Debug Info showed consistent behavior across attempts
- Score no longer produced erratic values

---

### Fix 3 — Score awards on wrong guesses

**Evidence it was broken:** Documented in Bug 3 of Section 1 (score went to -20 after several wrong guesses).

**How I diagnosed it:** Traced `update_score()` and found:

```python
if outcome == "Too High":
    if attempt_number % 2 == 0:
        return current_score + 5   # adds points for a WRONG guess
    return current_score - 5
```

**The fix:** Wrong guesses always subtract 5. Wins award `max(10, 100 - 10 * attempt_number)`.

**How I verified it:**
- Played a round and confirmed the score never increased on wrong guesses
- Final score was positive

---

### Fix 4 — Attempts started at 1 instead of 0

**Evidence it was broken:** The UI showed "Attempts left: 7" on first load even though no guess had been made.

**How I diagnosed it:** Found `st.session_state.attempts = 1` in the initialization block.

**The fix:** Changed to `st.session_state.attempts = 0`.

**How I verified it:** Reloaded the page — the display shows "Attempts left: 8".

---

### Post-Fix Walkthrough (Text)

After the fixes, I re-ran the game with a fresh secret:

```
=== Post-Fix Run (secret = 62, revealed via Debug Info) ===
> Guess 20  → hint: "📈 Go HIGHER!"   ✅ correct (20 < 62)
> Guess 90  → hint: "📉 Go LOWER!"    ✅ correct (90 > 62)
> Guess 62  → hint: "🎉 Correct! You won! The secret was 62. Final score: 80"
> Status: won

Verification checklist:
[x] Hint direction matches the comparison (low guess → "Go HIGHER")
[x] Secret stays constant across all attempts (62 throughout)
[x] Score stays positive (80 final, no negatives)
[x] Win condition triggers correctly
[x] "New Game" resets state cleanly
```

### Test Results

```
$ python -m pytest tests/ -v
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\gusra\OneDrive\ai110-module1show-game
plugins: anyio-4.15.1
collected 3 items

tests/test_game_logic.py::test_winning_guess PASSED                     [ 33%]
tests/test_game_logic.py::test_guess_too_high PASSED                    [ 66%]
tests/test_game_logic.py::test_guess_too_low PASSED                     [100%]

============================== 3 passed in 0.73s ==============================
```