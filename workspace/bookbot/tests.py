from stats import count_words, count_chars

def test(actual, expected):
    if actual == expected:
        print("  PASS")
    else:
        print(f"  FAIL — expected: {expected}, got: {actual}")

# count_words
print("count_words")

# empty string returns 0
test(count_words(""), 0)
# single word
test(count_words("hello"), 1)
# multiple words separated by spaces
test(count_words("the quick brown fox"), 4)
# leading and trailing whitespace
test(count_words("  hello world  "), 2)
# multiple spaces between words
test(count_words("one  two   three"), 3)
# newlines count as separators
test(count_words("line one\nline two\nline three"), 6)
# punctuation attached to words still counts as one word
test(count_words("hello, world!"), 2)


# count_chars
print("\ncount_chars")

# empty string returns empty dict
test(count_chars(""), {})
# single lowercase letter
test(count_chars("a"), {"a": 1})
# uppercase letters are counted as lowercase
test(count_chars("Aa"), {"a": 2})
# spaces are not counted
test(count_chars("a b"), {"a": 1, "b": 1})
# digits are not counted
test(count_chars("a1b2"), {"a": 1, "b": 1})
# punctuation is not counted
test(count_chars("hello, world!"), {"h": 1, "e": 1, "l": 3, "o": 2, "w": 1, "r": 1, "d": 1})
# only letters make it into the result
test(count_chars("abc123!@#"), {"a": 1, "b": 1, "c": 1})
# correct counts for a short sentence
test(count_chars("the cat"), {"t": 2, "h": 1, "e": 1, "c": 1, "a": 1})