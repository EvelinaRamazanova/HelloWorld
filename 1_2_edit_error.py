import json
import re
import tqdm as tqdm
from collections import Counter

PATH = '/Users/Evelina/Desktop/'
MAIN_WORDS = 'data_search_typos/opcorpora.txt'


# чтение строки файла
def dictionary_words(path):
    dictionary = set()
    for line in open(path, 'r').read().split('\n'):
        dictionary.add(line)
    ln = len(dictionary)
    print('Сформировал словарь (Длина: {})'.format(ln))
    return dictionary
########################################################################################################################


def words(text): return re.findall(r'\w+', text.lower())


WORDS = Counter(words(open(PATH+MAIN_WORDS).read()))


def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N


def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)


def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


i = 0
with open(PATH+'data_search_typos/save_opechatki.txt', 'r') as reader, open(PATH+'file.txt', 'w') as wrt:
    for string_errors in reader.readlines():
        w = string_errors.split(' ')[0]
        check = string_errors.split(' ')[1]

        print(i, '{} - {} {}\n'.format(w, correction(w), check))
        wrt.write('{} - {} {}\n'.format(w, correction(w), check))

        i += 1