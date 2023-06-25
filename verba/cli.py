from verba.load import load_words, load_keys
from verba.user_input import read_latin_input
from verba.word.word_key import WordKey as WK
from verba.console import console
from verba.generator_setup import select_generator_settings, create_generator

def answer_question(question):
    console.print(question.get_question_text(), style='verba.question')
    while True:
        submission = read_latin_input() 
        if submission == 'all':
            console.print(question.get_pofs_text())
            console.print(question.get_key_text())
            console.print(question.get_meaning_text())
            continue
        if submission == 'pofs':
            console.print(question.get_pofs_text())
            continue
        if submission == 'key':
            console.print(question.get_key_text())
            continue
        if submission == 'def':
            console.print(question.get_meaning_text())
            continue
        if submission == 'x':
            raise SystemExit(0)

        response = question.check_submissions(submission.split(','))
        if response == 'correct':
            console.print('[bold green]Correct!')
            return
        if response == 'wrong':
            console.print(f'[bold red]Wrong.[/] Answer: "{question.get_answers_text()}"')
            return
        if response == 'partial':
            console.print('[bold yellow]Partially Correct.')
            continue
        if response == 'answer':
            console.print(f'Answer: "{question.get_answers_text()}"')

def main():
    keys = load_keys('LL')
    words = load_words('LL')
    settings = select_generator_settings()
    generator = create_generator(settings, words, keys)

    for question in generator:
        answer_question(question)
        console.rule("")

if __name__ == '__main__':
    main()
