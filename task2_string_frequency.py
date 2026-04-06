def count_character_frequency(input_string: str) -> str:
    """
    Counts character occurrences in a string and outputs them in
    the order of their first appearance.

    Time Complexity: O(n) - We traverse the string once.
    Space Complexity: O(k) - Where k is the number of unique characters.
    """
    # Edge Case: Handle empty or None input
    if not input_string:
        return "Input string is empty."

    # Use a dictionary to store counts (Python 3.7+ preserves insertion order)
    frequency = {}

    for char in input_string:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    # Format the dictionary into the required output string
    # Example Output: h:1, e:1, l:3...
    result = ", ".join([f"{char}:{count}" for char, count in frequency.items()])
    return result


if __name__ == "__main__":
    # Test with the challenge example
    test_input = "hello world"
    print(f"Input: {test_input}")
    print(f"Output: {count_character_frequency(test_input)}")