from textblob import Word
import itertools
import re
import fileinput  # to store the  backup of the original  file
""" todo later 
add support for markdown
add the ability for the user to specify custom words and phrases that shouldn't trigger an error
Smart detection of metadata and technical things like links and HTML and CSS and code fences in Markdown
Make it interactive with corrections
Make a GUI
"""
filename = "error.txt"

#function for the argument parser

#
#function to read each word from file
def read_words(file_des):
    # noinspection PyTypeChecker
    byte_stream = itertools.groupby(itertools.takewhile(lambda c: bool(c), map(file_des.read, itertools.repeat(1))),
                                    str.isspace)
    words =("".join(group) for pred, group in byte_stream if not pred)
    words = [re.sub(r'[^A-Za-z0-9]+', ' ', word.lower()) for word in words]
    return words

#functio to correct the error in file.txt
def correct_word_spelling(word):
    word = Word(word)
    result = word.correct()
    #print(f"{word} was change to {result}")
    return result


#function to check for error in file.txt
def check_word_spelling(word):
    word = Word(word)
    result = word.spellcheck()
    if word == result[0][0]:
        pass
    else:
        find_word_location(filename, word)
        file_write(filename, word)

#function to write the correct word in file.txt
def file_write(filename, target_word, flags=0):
    correct_word = correct_word_spelling(target_word)
    with open(filename, "r+") as file:
        #read the file contents
        file_contents = file.read()
        text_pattern = re.compile(re.escape(target_word), flags)
        file_contents = text_pattern.sub(correct_word, file_contents)
        file.seek(0)
        file.truncate()
        file.write(file_contents)
# def file_write(filename, target_word):
#     correct_word = correct_word_spelling(target_word)
#     with fileinput.FileInput(filename, inplace=True, backup='.bak') as f:
#         for line in f:
#             if (target_word in line):
#                 line.replace(target_word, correct_word)
#                 #print(line.replace(target_word, correct_word), end='')
#             else:
#                 print("Nothing to change")
#funtion to get typo position
def find_word_location(filename,target_word):
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
                print(f"{target_word} found at Line {line_number}, Column {column_number} seems to be wrong ")
            except ValueError:
                # The word is not in this line
                pass
            line_number += 1
#function to read from file.txt
def file_reader(filename):
    """
    we should be separating by whitespace or reading each word in a sense
    """
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as f:
        with open(filename, "r") as fd:

            for word in read_words(fd):
                check_word_spelling(word)





file_reader(filename)
