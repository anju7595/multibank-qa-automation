import pytest
from task2_string_frequency import count_character_frequency

@pytest.mark.parametrize("input_val, expected_output", [
    ("hello world", "h:1, e:1, l:3, o:2,  :1, w:1, r:1, d:1"),
    ("MultiBank", "M:1, u:1, l:1, t:1, i:1, B:1, a:1, n:1, k:1"),
    ("!!!", "!:3"),
    ("", "Input string is empty.")
])
def test_string_logic(input_val, expected_output):
    assert count_character_frequency(input_val) == expected_output