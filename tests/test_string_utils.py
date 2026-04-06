import pytest
from task2_string_frequency import count_character_frequency


@pytest.mark.parametrize("input_string, expected_frequency", [
    # Standard sentence with spaces
    ("hello world", "h:1, e:1, l:3, o:2,  :1, w:1, r:1, d:1"),

    # Case sensitivity check (M vs m)
    ("MultiBank", "M:1, u:1, l:1, t:1, i:1, B:1, a:1, n:1, k:1"),

    # Special characters
    ("!!!", "!:3"),

    # Boundary condition: Empty string
    ("", "Input string is empty."),

    # Boundary condition: Single character
    ("a", "a:1")
], ids=["standard_phrase", "case_sensitivity", "special_chars", "empty_string", "single_char"])
def test_character_frequency_logic(input_string, expected_frequency):
    """
    Verifies the character frequency counter correctly identifies
    occurrences across various string patterns and boundary conditions.
    """
    # Act
    actual_result = count_character_frequency(input_string)

    # Assert
    assert actual_result == expected_frequency, (
        f"Failed for input: '{input_string}'. "
        f"Expected '{expected_frequency}' but got '{actual_result}'"
    )