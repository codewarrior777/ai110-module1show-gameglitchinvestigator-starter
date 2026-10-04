from logic_utils import check_guess, parse_guess


# ----------------------------------------------------------------------
# Core behavior tests (existing)
# ----------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# ----------------------------------------------------------------------
# Challenge 1: Advanced Edge-Case Testing
# ----------------------------------------------------------------------

def test_parse_guess_rejects_non_numeric_input():
    """
    Edge case: non-numeric string like "abc".
    A user could type letters by mistake. The parser should refuse
    to convert and return an error message instead of crashing.
    """
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_rejects_empty_input():
    """
    Edge case: empty string "".
    If the user clicks Submit without typing anything, the parser
    should reject it cleanly with a helpful message.
    """
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_converts_float_string_to_int():
    """
    Edge case: decimal written as a string like "3.7".
    The parser should truncate to the integer part (3) rather than
    crash on int("3.7"). This mirrors the original parse_guess logic.
    """
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None