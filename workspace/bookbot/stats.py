def get_words_count(content):
    words = content.split()
    return len(words)

def get_char_count(content):
    content = content.lower()
    char_count = {}
    for char in content:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    return char_count

def sort_on(tuple):
    return tuple[1]

def chars_dict_to_sorted_list(char_count):
    i = 0
    char_list = []
    for char in char_count:
        count = char_count[char]
        char_list.append((char, count))
    sorted_char_list = sorted(char_list, reverse=True, key=sort_on)
    return sorted_char_list