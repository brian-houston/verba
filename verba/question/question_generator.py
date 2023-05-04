import random

class QuestionGenerator:
    def __init__(self):
        pass

    def choices(population, k=1):
        return random.choices(population, k=k)

    def choice(population):
        return random.choice(population)
