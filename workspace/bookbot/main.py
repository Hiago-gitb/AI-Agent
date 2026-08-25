import sys
from stats import get_words_count, get_char_count, chars_dict_to_sorted_list
from bot import get_book_text, print_report
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)
    path_to_book = sys.argv[1]
    file_path = get_book_text(path_to_book)
    with open(file_path) as file:
        content = file.read()
        num_words = get_words_count(content)
        char_count = get_char_count(content)
        sorted_list = chars_dict_to_sorted_list(char_count)
        print_report(file_path, num_words, sorted_list)

main()