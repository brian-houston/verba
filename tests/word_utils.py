from verba.word.noun import Noun
import verba.word.make as make

def make_word(pofs, pps, ch='1', meaning='', keywords=''):
    data = {
            'chapter': ch,
            'part_of_speech': pofs,
            'pp1': pps[0],
            'pp2': pps[1],
            'pp3': pps[2],
            'pp4': pps[3],
            'meaning': meaning,
            'keywords': keywords,
            }

    return make.make_word(data)

