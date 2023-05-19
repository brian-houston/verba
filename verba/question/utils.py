import random

# factor a word's weight is multiplied by if it is chosen
falloff = 0.33

def inflection_generator(words, inflection_keys):
    fails = 0
    weights = [1 for _ in words]
    n_words = len(words)
    while True:
        # stop if all weights are zero
        # or words is empty
        if fails == n_words:
            return StopIteration()

        i = random.choices(range(n_words), weights=weights)[0]
        word = words[i]
        pofs = word.part_of_speech
        possible_inflection_keys = None
        if pofs not in inflection_keys:
            possible_inflection_keys = word.get_inflection_keys()
        else:
            possible_inflection_keys = set(inflection_keys[pofs]).intersection(word.get_inflection_keys())
            possible_inflection_keys = list(possible_inflection_keys)

        if not possible_inflection_keys:
            fails += 1
            weights[i] = 0 
            continue

        weights[i] *= falloff 
        selected_key = random.choice(possible_inflection_keys)

        yield (word, selected_key)
