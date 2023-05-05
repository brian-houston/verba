import csv
from importlib.resources import files

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
            for gender in line['gender'].split():
                key = (line['declension'], gender, line['case'], line['number'])
                endings['noun'][key] = line['ending']

load_endings()
