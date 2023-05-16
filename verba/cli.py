import csv
import verba.word.load_words as load_words
from verba.input import read_latin_input
from verba.question.vocab import vocab_question_generator 
from verba.question.macron import macron_question_generator 
from verba.question.identify import identify_question_generator 
from verba.word.word_key import WordKey as WK
from verba.console import console
from rich.panel import Panel

arg_ask_user_text = {
        'level': "Up to what chapter's level of grammer do you want to practice? ",
        'chapters': "What chapters' vocabulary lists do you want to practice? ",
        'attributes': "What attributes do you want to identify? ",
        'match': "What parts of speech do you want to match? ",
        'filters': "How do you want to filter the words selected? ",
        }

question_types_arg_list = {
        'identify': ['level', 'chapters', 'attributes', 'filters'],
        'compose': ['level', 'chapters', 'filters'],
        'vocab': ['level', 'chapters', 'filters'],
        'macron': ['level', 'chapters', 'filters'], 
        'matching': ['level', 'chapters', 'match', 'filters'], 
        }

def to_int_or_none(x):
    try:
        return int(x)
    except:
        return None

def translate_arg_input(arg, input):
    if arg == 'level':
        try:
            return int(input)
        except:
            return None
    if arg == 'chapters':
        try:
            chapters = set()
            for s in input.replace(',', ' ').split():
                digits = s.split('-')
                if len(digits) == 1:
                    chapters.add(int(digits[0]))
                elif len(digits) == 2:
                    start = int(digits[0])
                    end = int(digits[1]) + 1
                    chapters.update(range(start, end))
            return chapters
        except:
            return None
    if arg == 'filters':
        try:
            filters = {}
            for s in input.split(','):
                s = s.strip()
                if ':' not in s:
                    filters[s] = ['all'] 
                    continue
                parts = s.split(':')
                part_of_speech = parts[0]
                keywords = parts[1].split()
                filters[part_of_speech] = keywords if keywords else ['all']
            return filters
        except:
            return None
    if arg == 'attributes':
        try:
            attr_table = {}
            for s in input.split(','):
                s = s.strip()
                parts = s.split(':')
                part_of_speech = parts[0]
                attributes = parts[1].split()
                if not attributes:
                    return None
                attr_table[part_of_speech] = attributes 
            return attr_table
        except:
            return None

    return "Nothing"

def select_generator_args():
    question_type = ''
    while True:
        question_type = input('What type of question do you want to practice? ')
        if question_type in question_types_arg_list:
            break
        console.print("What you entered is not valid, so let's try again.")

    args = {}
    args['type'] = question_type
    for arg_name in question_types_arg_list[question_type]:
        while True:
            value = translate_arg_input(arg_name, input(arg_ask_user_text[arg_name]))
            if value:
                args[arg_name] = value
                break
            console.print("What you entered is not valid, so let's try again.")

    return args

def create_generator(args, words, keys):
    if args['type'] == 'macron':
        return macron_question_generator(words, keys)
    if args['type'] == 'vocab':
        return vocab_question_generator(words, keys)
    if args['type'] == 'identify':
        return identify_question_generator(words, keys, args['attributes'])

def answer_question(question):
    console.print(question.get_question_text(), style='verba.question')
    while True:
        submission = read_latin_input() 
        if submission == 'def':
            console.print(question.get_meaning_text())
            continue
        elif submission == 'x':
            raise SystemExit(0)
        response = question.check_submissions([submission])
        if response == 'correct':
            console.print('[bold green]Correct!')
            return
        if response == 'wrong':
            console.print('[bold red]Wrong.')
            return
        if response == 'partial':
            console.print('[bold yellow]Partially Correct.')
            continue
        if response == 'continue':
            console.print(f'The answer is "{question.get_answers_text()}". Input "c" if you were correct and anything else otherwise.')

def main():
    args = select_generator_args()
    words = load_words.load_words('LL')
    words = [w for w in words if w.chapter == 10]
    keys = [WK('acc', 's')]
    generator = create_generator(args, words, keys)

    for question in generator:
        answer_question(question)

if __name__ == '__main__':
    main()
