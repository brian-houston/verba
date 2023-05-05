import csv
import verba.word.load_words as load_words
import verba.input as input
import verba.word.endings as endings
from verba.question.identify_generator import IdentifyGenerator


def main():
    words = load_words.load_words('LL')
    gen = IdentifyGenerator('noun', ['gender'], [('nom', 's')])
    iter = gen.generate(words)

    while True:
        question = next(iter)
        question.print_english()
        submission = input.read_latin_input()
        print(question.check_submissions([submission]))


if __name__ == '__main__':
    main()
