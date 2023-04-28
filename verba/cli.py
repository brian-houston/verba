import csv
from importlib.resources import files
import verba.word.endings as endings
import verba.input as input
from verba.word.noun import Noun

def get_words(library_name):
    words = []

    with files('verba.data').joinpath(library_name).joinpath('nouns.tsv').open(encoding='utf-16') as file:
        tsv_file = csv.DictReader(file, delimiter='\t')
        for line in tsv_file:
            words.append(Noun(line))

    return words

def main():
    endings.load_endings()
    get_words('LL')
    print(endings.endings)
    word = input.read_latin_input()
    print(word)

if __name__ == '__main__':
    main()
