import csv

endings = {
        'noun': {},
        'verb': {},
        'adjective': {},
        }

def load_endings():
    global endings, endings_repeats

    with open('verbae/data/noun_endings.tsv', encoding='utf-16') as file:
        tsv_file = csv.DictReader(file, delimiter='\t')
        for line in tsv_file:
            key = f"{line['declension']}-{line['gender']}-{line['case']}-{line['number']}"
            endings['noun'][key] = line['ending']
