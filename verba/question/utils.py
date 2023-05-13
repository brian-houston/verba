import random

def inflection_generator(words, inflection_keys):
    fails = 0
    while True:
        if fails > 10:
            return StopIteration()

        word = random.choice(words)
        possible_inflection_keys = set(inflection_keys).intersection(word.get_inflection_keys())
        possible_inflection_keys = list(possible_inflection_keys)

        if not possible_inflection_keys:
            fails += 1
            continue
        else: 
            fails = 0

        selected_key = random.choice(possible_inflection_keys)

        yield (word, selected_key)
