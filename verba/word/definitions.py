parts_of_speech = ['noun', 'verb', 'adjective']

value_to_attribute = {}

def add_values(values, attribute):
    global value_to_attribute
    for v in values:
        value_to_attribute[v] = attribute

noun_declensions = ['1', '2', '3', '4', '5']
verb_conjugations = ['1', '2', '3', '4']
adjective_declensions = ['1/2', '3']
genders = ['f', 'm', 'n']
noun_subgroups = ['reg', 'i-stem', 'short-e']
adjective_subgroups = ['reg', 'ius']
cases = ['nom', 'acc', 'gen', 'dat', 'abl']
numbers = ['s', 'p']
voices = ['act', 'pass']
tenses = ['pres', 'fut', 'imperf', 'perf', 'futp', 'plup']
moods = ['ind', 'subj', 'impera']
degrees = ['pos', 'comp', 'super']
persons = ['1st', '2nd', '3rd']

key_order = ['group', 'subgroup', 'degree', 'mood', 'tense', 'voice', 'person', 'gender', 'case', 'number']

add_values(noun_declensions, 'group')
add_values(verb_conjugations, 'group')
add_values(adjective_declensions, 'group')
add_values(noun_subgroups, 'subgroup')
add_values(adjective_subgroups, 'subgroup')
add_values(genders, 'gender')
add_values(cases, 'case')
add_values(numbers, 'number')
add_values(voices, 'voice')
add_values(tenses, 'tense')
add_values(moods, 'mood')
add_values(degrees, 'degree')
add_values(persons, 'person')
