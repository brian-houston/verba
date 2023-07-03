import itertools

def line_product(line):
    line = {k: v.split() for k, v in line.items()}
    line = {k: v for k, v in line.items() if v}
    for p in itertools.product(*line.values()):
        yield dict(zip(line.keys(), p))
