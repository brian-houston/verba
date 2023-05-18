import verba.word.load_words as load_words
from verba.input import read_latin_input
from verba.word.word_key import WordKey as WK
from verba.console import console
from verba.generator_setup import select_generator_settings, create_generator

def answer_question(question):
    console.print(question.get_question_text(), style='verba.question')
    while True:
        submission = read_latin_input() 
        if submission == 'def':
            console.print(question.get_meaning_text())
            continue
        elif submission == 'x':
            raise SystemExit(0)
        response = question.check_submissions(submission.split(','))
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
    words = load_words.load_words('LL')
    settings = select_generator_settings()
    keys = [WK('acc', 's')]
    generator = create_generator(settings, words, keys)

    for question in generator:
        answer_question(question)

if __name__ == '__main__':
    main()
