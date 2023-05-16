from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme

class QuotesHighlighter(RegexHighlighter):
    base_style = 'verba.'
    highlights = [r'(?P<quotes>".*?")']

theme = Theme({'verba.quotes': 'bold', 'verba.question': ''})
console = Console(highlighter=QuotesHighlighter(), theme=theme)
