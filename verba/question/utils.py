import random

def inflection_generator(words, inflection_keys):
    fails = 0
    successes = 0
    n_words = len(words)

    weights = [1 for _ in words]
    weights_init = [1 for _ in words]
    while True:
        # stop if all weights are zero
        # or words is empty
        if fails == n_words:
            return StopIteration()

        if successes + fails == n_words:
            weights = weights_init.copy()
            successes = 0

        i = random.choices(range(n_words), weights=weights)[0]
        word = words[i]
        pofs = word.part_of_speech

        possible_inflection_keys = None
        if word.is_inflected and pofs in inflection_keys:
            possible_inflection_keys = inflection_keys[pofs].intersection(word.get_inflection_keys())
        else:
            possible_inflection_keys = word.get_inflection_keys()
        possible_inflection_keys = list(possible_inflection_keys)

        if not possible_inflection_keys:
            fails += 1
            weights[i] = 0 
            weights_init[i] = 0
            continue

        weights[i] = 0
        successes += 1
        selected_key = random.choice(possible_inflection_keys)

        yield (word, selected_key)

def double_inflection_generator(words, inflection_keys):
    fails = 0
    successes = 0
    n_words = len(words)

    weights = [1 for _ in words]
    weights_init = [1 for _ in words]
    while True:
        # stop if all weights are zero
        # or words is empty
        if fails == n_words:
            return StopIteration()

        if successes + fails == n_words:
            weights = weights_init.copy()
            successes = 0

        i = random.choices(range(n_words), weights=weights)[0]
        word = words[i]
        pofs = word.part_of_speech

        possible_inflection_keys = None
        if word.is_inflected and pofs in inflection_keys:
            possible_inflection_keys = inflection_keys[pofs].intersection(word.get_inflection_keys())
        else:
            possible_inflection_keys = word.get_inflection_keys()
        possible_inflection_keys = list(possible_inflection_keys)

        if len(possible_inflection_keys) < 2:
            fails += 1
            weights[i] = 0 
            weights_init[i] = 0
            continue

        weights[i] = 0
        successes += 1
        selected_keys = random.sample(possible_inflection_keys, 2)

        yield (word, selected_keys[0], selected_keys[1])
