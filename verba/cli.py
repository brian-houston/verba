from verba.load import load_words, load_keys
from verba.console import console
from verba.setup import select_generator_settings, create_generator
from verba.parser import parser
from importlib.resources import files
import json

def answer_question(question, settings):
    console.print(question.get_question_text(), style='verba.question')
    if settings['hints']:
        console.print(question.get_pofs_text())
        console.print(question.get_key_text())
        console.print(question.get_meaning_text())

    while True:
        submission = input()
        if submission == '*':
            console.print(question.get_pofs_text())
            console.print(question.get_key_text())
            console.print(question.get_meaning_text())
            continue
        if submission == 'pofs':
            console.print(question.get_pofs_text())
            continue
        if submission == 'wk':
            console.print(question.get_key_text())
            continue
        if submission == 'def':
            console.print(question.get_meaning_text())
            continue
        if submission == 'x':
            raise SystemExit(0)

        response = question.check_submissions(submission.split(','), ignore_macrons=settings['ignore_macrons'])
        if response == 'correct':
            console.print('[bold green]Correct!')
            return
        if response == 'wrong':
            console.print(f'[bold red]Wrong.[/] Answer: "{question.get_answers_text()}"')
            return
        if response == 'answer':
            console.print(f'Answer: "{question.get_answers_text()}"')

def main():
    settings = {}
    args = parser.parse_args()
    if args.filename:
        try:
            io = open(args.filename, 'r')
            try:
                settings = json.load(io)
            except:
                raise SystemExit('Unable to load JSON file')
            io.close()
        except:
            raise SystemExit('Failed to open file')

    key_path = files('verba.data').joinpath('LL').joinpath('keys.tsv')
    words_path = files('verba.data').joinpath('LL').joinpath('words.tsv')
    if 'keys_file' in settings:
        key_path = args.filename.parents[0].joinpath(settings['keys_file'])
    elif args.preset:
        key_path = files('verba.data').joinpath(args.preset).joinpath('keys.tsv')

    if 'words_file' in settings:
        words_path = args.filename.parents[0].joinpath(settings['words_file'])
    elif args.preset:
        words_path = files('verba.data').joinpath(args.preset).joinpath('words.tsv')

    keys = None
    try:
        keys = load_keys(key_path)
    except:
        raise SystemExit('Failed to open keys file')

    words = None
    try:
        words = load_words(words_path)
    except:
        raise SystemExit('Failed to open words file')

    if not settings:
        settings = select_generator_settings()

    generator = create_generator(settings, words, keys)

    if not generator:
        return


    settings['hints'] = args.hints
    settings['ignore_macrons'] = args.ignore_macrons

    for question in generator:
        answer_question(question, settings)
        console.rule("")

if __name__ == '__main__':
    main()
