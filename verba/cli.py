import csv
from importlib.resources import files
import verba.word.endings as endings
import verba.word.load_words as load_words
import verba.input as input
from verba.word.noun import Noun


def main():
    load_words.load_words('LL')
    print(endings.endings)
    word = input.read_latin_input()
    print(word)

if __name__ == '__main__':
    main()
