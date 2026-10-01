# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [X] Describe the game's purpose.
- [X] Detail which bugs you found.
- [X ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

## Demo Walkthrough

1. User opens the app. A random secret number is generated within the difficulty's range (1–100 on Normal).
2. User enters a guess of 80. The game shows "📉 Go LOWER!" because 80 is higher than the secret.
3. User enters a guess of 20. The game shows "📈 Go HIGHER!" because 20 is lower than the secret.
4. Score decreases by 5 after each wrong guess.
5. User enters the correct secret. The game shows "🎉 Correct!", awards the win bonus, and ends the round.
6. User clicks "New Game" to reset the score and pick a fresh secret.
**Screenshot** 
![Winning game](screenshot_winning_game_AI_2026.png)

**Demo video**: [Watch the winning moment 🎉]( video_winning_game_AI_2026.mp4)

## 🧪 Test Results

============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\gusra\OneDrive\ai110-module1show-game
plugins: anyio-4.15.1
collected 3 items

tests/test_game_logic.py::test_winning_guess PASSED                     [ 33%]
tests/test_game_logic.py::test_guess_too_high PASSED                    [ 66%]
tests/test_game_logic.py::test_guess_too_low PASSED                     [100%]

============================== 3 passed in 0.73s ==============================


## 🚀 Stretch Features

- [X] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
