from textblob import Word
import itertools

""" todo later
add support for markdown
add the ability for the user to specify custom words and phrases that shouldn't trigger an error
Smart detection of metadata and technical things like links and HTML and CSS and code fences in Markdown
Make it interactive with corrections
Make a GUI
"""


#function for the argument parser
#
#function to read each word from file
def read_words(file_des):
    # noinspection PyTypeChecker
    byte_stream = itertools.groupby(itertools.takewhile(lambda c: bool(c), map(file_des.read, itertools.repeat(1))),
                                    str.isspace)
    return ("".join(group) for pred, group in byte_stream if not pred)


#functio to correct the error in file.txt
def correct_word_spelling(word):
    word = Word(word)
    result = word.correct()
    return result


#function to check for error in file.txt
def check_word_spelling(word):
    word = Word(word)

    result = word.spellcheck()

    if word == result[0][0]:
        pass
    else:
        correct_word_spelling(word)
        print(f'Spelling of "{word}" is not correct!')

#funtion to get typo position
# def get_typo_position(word):
#     with open('Path/to/file', 'r') as f:
#         content = f.read()
#         print (content.index('test'))

#function to write the correct word in file.txt
def file_write(file):
    with open(file, "w"):
        pass


#function to read from file.txt
def file_reader(file):
    """
    we should be separating by whitespace or reading each word in a sense
    """
    with open(file, "r") as fd:
        for word in read_words(fd):
            check_word_spelling(word)


def find_word_location(filename, target_word):
    with open(filename, 'r', encoding='utf-8') as file:
        line_number = 1
        for line in file:
            # Split the line into words to find the exact match and column position
            words = line.split()
            try:
                # Try to find the word in the split words to get the index
                word_index = words.index(target_word)
                # Calculate the column by joining the words with spaces and finding the position
                column_number = len(' '.join(words[:word_index])) + (1 if word_index > 0 else 0)
                print(f"Word found at Line {line_number}, Column {column_number}")
            except ValueError:
                # The word is not in this line
                pass

            line_number += 1

find_word_location('error.txt','memory')
#file_reader('error.txt')
