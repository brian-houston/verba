import csv
import itertools
from importlib.resources import files
from verba.word.word_key import WordKey as WK

def line_product(line):
    line = {k: v.split() for k, v in line.items()}
    line = {k: v for k, v in line.items() if v}
    for p in itertools.product(*line.values()):
        yield dict(zip(line.keys(), p))

endings = {
        }

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
