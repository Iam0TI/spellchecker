from textblob import Word
import itertools
import re
import optparse
import fileinput  # to store the  backup of the original  file

""" todo later 
add support for markdown
add the ability for the user to specify custom words and phrases that shouldn't trigger an error
Smart detection of metadata and technical things like links and HTML and CSS and code fences in Markdown
Make it interactive with corrections (done)
Make a GUI
"""
filename = "error.txt"


#function for the argument parser
def option_parser():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--txt", dest="text_file", help="The option for working with text file")
    parser.add_option("-m", "--ma", dest="markdown_file", help="The option for working with markdown file")
    (options, arguments) = parser.parse_args()

    if not options.text_file:
        parser.error("type PYTHON3 spellcheck.py --HELP")
    elif not options.markdown_file:
        parser.error("type PYTHON3 spellcheck.py --HELP ")
    return options

#function to read each word from file
def read_words(file_des: str):
    # noinspection PyTypeChecker
    byte_stream = itertools.groupby(itertools.takewhile(lambda c: bool(c), map(file_des.read, itertools.repeat(1))),
                                    str.isspace)
    words = ("".join(group) for pred, group in byte_stream if not pred)
    words = [re.sub(r'[^A-Za-z0-9]+', '', word.lower()) for word in words]
    return words


#functio to correct the error in file.txt
def correct_word_spelling(word) -> str:
    word: str = Word(word)
    result: str = word.correct()
    print(f"{word} was change to {result}")
    return result

#funtion to get typo position
def find_word_location(filename, target_word) -> None:
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

#function to write the correct word in file.txt
def file_write(filename, target_word, writing_mode :int,replace_with="nan", flags=0):
    # the writing mode variable is  to tell us which correction mode to use
    if writing_mode == 0:
        correct_word = correct_word_spelling(target_word)
    elif writing_mode == 1 :
        correct_word = replace_with
    with open(filename, "r+") as file:
        #read the file contents
        file_contents = file.read()
        text_pattern = re.compile(re.escape(target_word), flags)
        file_contents = text_pattern.sub(correct_word, file_contents)
        file.seek(0)
        file.truncate()
        file.write(file_contents)
def choose_correction_mode(word):
    find_word_location(filename, word)
    confirm_edit =input(f'''
       The word "{word}" seem to be wrong enter.
       would you  like to correct  it ? Y/N.
    ''')
    if confirm_edit == 'Y' or  confirm_edit == 'y' or  confirm_edit == "yes" or  confirm_edit == 'Yes':

        while True:
            try :
                option = int (input('''
                    Choose from the 2 option to edit the word:
                    0 - auto correct
                    1 - replace with a given word 
                '''))
                if option in range(0,2):
                    break
                else :
                    print(f"option must be 0 or 1")
            except ValueError:
                    print(" Option must be  an integer")

        if option == 0:
            print("autocorrecting.................")
            correct_word_spelling(word)
            file_write(filename, word ,option)

        elif option == 1:
            given_word = str((input(" Enter new word :  ")))
            file_write(filename, word , option, given_word)

# function to check for error in file.txt
def check_word_spelling(word):
    word = Word(word)
    result = word.spellcheck()
    if word == result[0][0]:
        pass
    else:
        choose_correction_mode(word)

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
