import csv
import itertools
from importlib.resources import files
from verba.word.word_key import WordKey as WK
from verba.utils import line_product

endings = {}

def load_endings():
    global endings 

    with files('verba.data').joinpath('endings.tsv').open(encoding='utf-16') as file:
        tsv_file = csv.DictReader(file, delimiter='\t')
        for line in tsv_file:
            pofs = line['part_of_speech']
            if pofs == '#':
                continue

            endings.setdefault(pofs, {})
            for lp in line_product(line):
                key = WK(*[v for k,v in lp.items() if k not in ['ending', 'part_of_speech']]) 
                endings[pofs][key] = line['ending']

load_endings()
