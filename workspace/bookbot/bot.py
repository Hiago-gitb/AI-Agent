import json

def get_book_text(path):
    return path

def print_report(book_path, word_count, sorted_list):
    print("============ BOOKBOT ============")
    print(f"Analyzing book found at {book_path}")
    print("----------- Word Count ----------")
    print(f"Found {word_count} total words")
    print("--------- Character Count -------")
    for i in sorted_list:
        if i[0].isalpha() == False:
            continue
        else:
            print(f"{i[0]}: {i[1]}")
    print("============= END ===============")
    return json.dumps(sorted_list, indent=2)