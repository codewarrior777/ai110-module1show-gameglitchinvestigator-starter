# Reflection — Game Glitch Investigator

## 1. What was broken when you started?

I forked and ran the original `app.py` and found four distinct bugs:

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

**Bug 2 — Secret silently converted to a string on even attempts**
Inside the submit handler:
```python
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)