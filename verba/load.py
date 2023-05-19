import csv
from importlib.resources import files
from verba.word.noun import Noun

def load_keys(library_name):
    pass

def load_words(library_name):
    words = []

    with files('verba.data').joinpath(library_name).joinpath('nouns.tsv').open(encoding='utf-16') as file:
        tsv_file = csv.DictReader(file, delimiter='\t')
        for line in tsv_file:
            words.append(Noun(line))

    return words
