parts_of_speech = ['noun', 'verb', 'adjective']
genders = ['f', 'm', 'n']
declensions = ['1', '2', '3', '4', '5']
cases = ['nom', 'acc', 'gen', 'dat', 'abl']
numbers = ['s', 'p']

inflections_lookup = {
        'noun': {
                'case': 0,
                'number': 1,
                'gender': 'base',
                'declension': 'base',
            }
        }

attributes_order = {
        'noun': ['gender', 'case', 'number'],
        'adjective': ['gender', 'case', 'number'],
        'verb': ['mood', 'tense', 'voice', 'person', 'number']
        'participle': ['tense', 'voice', 'gender', 'case', 'number'],
        }

value_to_attributes = {
            'f': 'gender',
            'm': 'gender',
            'n': 'gender',
            'nom': 'case',
            'acc': 'case',
            'gen': 'case',
            'dat': 'case',
            'abl': 'case',
            's': 'number',
            'p': 'number',
            'pres': 'tense',
            'fut': 'tense',
            'imperf': 'tense',
            'perf': 'tense',
            'futp': 'tense',
            'plup': 'tense',
            'ind': 'mood',
            'impera': 'mood',
            'subj': 'mood',
            '1st': 'person',
            '2nd': 'person',
            '3rd': 'person',
            'act': 'voice',
            'pas': 'voice',
        }
