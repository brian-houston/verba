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
def lower_latin(str):
    return ''.join([c.lower() if c not in long_upper_vowels else long_lower_vowels[long_upper_vowels.index(c)]
            for c in list(str)])

def demacronify(str):
    char_list = list(str)
    char_list = [c if c not in long_vowels else short_vowels[long_vowels.index(c)] 
            for c in char_list]
    return ''.join(char_list)