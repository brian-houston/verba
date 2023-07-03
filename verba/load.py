import csv
from importlib.resources import files
from verba.word.word_key import WordKey as WK
from verba.word.make import make_word
from verba.utils import line_product

def load_keys(library_name):
    keys = {}
    with files('verba.data').joinpath(library_name).joinpath('keys.tsv').open(encoding='utf-16') as file:
        tsv_file = csv.DictReader(file, delimiter='\t')
        for line in tsv_file:
            chapter = int(line['chapter'])
            pofs = line['part_of_speech']
            keys.setdefault(pofs, set())
            for lp in line_product(line):
                key = WK(*[v for k,v in lp.items() 
                           if k != 'chapter' and k != 'part_of_speech']) 
                keys[pofs].add((chapter, key))

    return keys

def load_words(library_name):
    words = []

    with files('verba.data').joinpath(library_name).joinpath('words.tsv').open(encoding='utf-16') as file:
        tsv_file = csv.DictReader(file, delimiter='\t')
        for line in tsv_file:
            line = {k: v.strip() for k, v in line.items()}
            word = make_word(line)
            if word:
                words.append(word)

    return words
