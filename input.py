import readchar

short_lower_vowels = ['a', 'e', 'i', 'o', 'u', 'y']
short_upper_vowels = ['A', 'E', 'I', 'O', 'U', 'Y']
long_lower_vowels = ['ā', 'ē', 'ī', 'ō', 'ū', 'ȳ'] 
long_upper_vowels = ['Ā', 'Ē', 'Ī', 'Ō', 'Ū', 'Ȳ']

short_vowels = short_lower_vowels + short_upper_vowels
long_vowels = long_lower_vowels + long_upper_vowels

# converts chars in char list to lowercase equivalents
# preserves macrons
# returns list of chars
def lower_latin(char_list):
    return [c.lower() if c not in long_upper_vowels else long_lower_vowels[long_upper_vowels.index(c)]
            for c in char_list]

# retrieves user input
# uses '-' key to toggle macron on vowels
# returns lowercase string with macrons preserved
def read_latin_input():
    char_list = []
    while True:
        c = readchar.readchar()
        if c == '\n':
            print('\n', end='', flush=True)
            break
        elif c == readchar.key.BACKSPACE:
            print('\b \b', end='', flush=True)
            if char_list:
                char_list.pop()
        elif c == '-':
            # toggle macron 
            if char_list[-1] in short_vowels:
                vowel = long_vowels[short_vowels.index(char_list[-1])]
                print('\b' + vowel, end='', flush=True)
                char_list[-1] = vowel 
            elif char_list[-1] in long_vowels:
                vowel = short_vowels[long_vowels.index(char_list[-1])]
                print('\b' + vowel, end='', flush=True)
                char_list[-1] = vowel 
        else:
            print(c, end='', flush=True)
            char_list += c

    return ''.join(lower_latin(char_list))

