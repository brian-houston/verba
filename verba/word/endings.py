import csv
import itertools
from importlib.resources import files

def line_product(line):
    line = {k: v.split() for k, v in line.items()}
    for p in itertools.product(*line.values()):
        yield dict(zip(line.keys(), p))

endings = {
        'noun': {},
        'verb': {},
        'adjective': {},
        }

def load_endings():
    global endings 

    with files('verba.data').joinpath('noun_endings.tsv').open(encoding='utf-16') as file:
        tsv_file = csv.DictReader(file, delimiter='\t')
        for line in tsv_file:
            for lp in line_product(line):
                key = (lp['declension'], lp['gender'], lp['category'], lp['case'], lp['number'])
                endings['noun'][key] = line['ending']

load_endings()
