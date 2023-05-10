import csv
import verba.word.load_words as load_words
import verba.input as input
import verba.word.endings as endings
from verba.question.identify_generator import IdentifyGenerator
from verba.question.macron_generator import MacronGenerator
from verba.question.vocab_generator import VocabGenerator
from verba.word.word_key import WordKey as WK


def main():
    words = load_words.load_words('LL')
    gen = VocabGenerator([WK('nom', 's'), WK('gen', 'p')])
    iter = gen.generate(words)

    while True:
        question = next(iter)
        question.print_english()
        submission = input.read_latin_input()
        print(question.check_submissions([submission]))

if __name__ == '__main__':
    main()
