from collections import OrderedDict


def count_character_frequency(input_string: str) -> str:
    """
    Counts character occurrences in a string and outputs them in
    the order of their first appearance.

    Time Complexity: O(n) - We traverse the string once (length n).
    Space Complexity: O(k) - Where k is the number of unique characters.
    """
    # Defensive programming: Handle None or empty strings
    if not input_string:
        return "Input string is empty."

    # Using a dictionary to maintain insertion order (Python 3.7+)
    frequency = {}

    for char in input_string:
        frequency[char] = frequency.get(char, 0) + 1

    # Using a generator expression within join for memory efficiency
    return ", ".join(f"{char}:{count}" for char, count in frequency.items())


if __name__ == "__main__":
    # Sample execution for verification
    test_cases = ["hello world", "MultiBank", "!!!", ""]

    for test in test_cases:
        print(f"Input:  '{test}'")
        print(f"Output: {count_character_frequency(test)}\n")