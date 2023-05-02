import csv
import verba.word.load_words as load_words
import verba.input as input


def main():
    load_words.load_words('LL')
    word = input.read_latin_input()
    print(word)

if __name__ == '__main__':
    main()
