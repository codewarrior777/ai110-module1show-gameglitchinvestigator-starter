# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- To be completed in Challenge 2 (Feature Expansion). -->

**What did the agent do?**

<!-- To be completed in Challenge 2 (Feature Expansion). -->

**What did you have to verify or fix manually?**

<!-- To be completed in Challenge 2 (Feature Expansion). -->

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
<!-- To be completed in Challenge 3 (Professional Documentation). -->
```

**Linting output before:**

```
<!-- To be completed in Challenge 3 (Professional Documentation). -->
```

**Changes applied:**

<!-- To be completed in Challenge 3 (Professional Documentation). -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- To be completed in Challenge 5 (AI Model Comparison). -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- To be completed in Challenge 5 (AI Model Comparison). -->