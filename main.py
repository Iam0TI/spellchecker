import nltk
nltk.download("punkt")

from nltk.tokenize import word_tokenize
file = open("error.txt",newline='' )
result = file.read()
words = word_tokenize(result)
for i in words:
       print(i)