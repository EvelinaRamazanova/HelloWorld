# -*- coding: utf8 -*-
import re
import json
import csv
import sys
import numpy as np
import nltk

csv.field_size_limit(sys.maxsize)
PATH = '/Users/Evelina/Desktop/'
KTC = 'database_ktc.csv'

DATA = 'data_search_typos/for_annotation.csv'
MAIN_WORDS = 'data_search_typos/dict_full.txt'

SAVE_OPECHATKI = 'data_search_typos/save_opechatki.txt'
SAVE_VER = 'data_search_typos/save_ver.txt'

PUNCTUATION = set('!"#$%№&(‘)’,‚*+,-./©``:;<=>?@[\]—^_`{|}~”°›||‹„“«»®')

# смотреть опечатки которые повторяются в документах больше N раз
N = 0
# смотреть процент опечаток выше M
M = 0


# чтение датасета с ктс
def dataset_ktc(path):
    with open(path, 'r') as ktc:
        for doc in csv.reader(ktc):

            if doc[2] == 'NULL':
                continue
            yield doc


# чтение строки файла словаря
def dictionary_words(path):
    f = open(path, 'r')
    file = f.read().split('\n')
    dictionary = set()
    for line in file:
        dictionary.add(line.lower())
    ln = len(dictionary)
    print('Сформировал словарь (Длина словаря: {})'.format(ln))
    return dictionary


# нахождение во вложенном словаре значение ключа "rus"
def find_from_doc_rus(doc):
    doc = json.loads(doc[2])
    lst = list()
    for val in doc.values():
        for block in val['blocks'].values():
            lst.append(block['content']['rus'])
    return lst


# нахождение знаков пунктуации, цифр, английких и словарных слов в документах
def find_punct_num_ss_eng(doc_word, dict_annotation):
    mistake = []
    for word in doc_word:
        if word in PUNCTUATION:
            continue
        elif word in re.findall(r'^\d+$', word):
            continue
        elif word in re.findall(r'[a-zA-Z]+', word):
            continue
        elif word in dict_annotation:
            continue
        else:
            mistake.append(word)
    return mistake


# вычисление вероятности появления опечаток
def find_ver(doc_word, mistake):
    ver = (len(mistake) / len(doc_word) * 100)
    return ver


# подсчет частоты встречаемости слова в тексте
def count_frequency_of_opechatki(dictionary):
    frequency = {}
    for word in dictionary:
        count = frequency.get(word, 0)
        frequency[word] = count + 1
    return frequency


# сортировка по частоте встречаемости и сохранение опечаток
def sort_delete_save(dict_for_sort, file, n):
    f = {k: v for k, v in dict_for_sort.items() if v > n}
    for k, v in sorted(f.items(), key=lambda x: x[1], reverse=True):
        file.write('{} ({})\n'.format(k, v))


# сортировка по частоте встречаемости и сохранение опечаток в (альтернативный формат)
def sort_delete_save_other_format(dict_for_sort, file, n):
    f = {k: v for k, v in dict_for_sort.items() if v > n}
    for k, v in sorted(f.items(), key=lambda x: x[1], reverse=True):
        file.write('Документ № {}, процент опечаток: {:.3f}%)\n'.format(k, v))


# подсчет колличества всех докуметов
def length(iteration):
    lt = []
    for i in range(1, iteration):
        lt.append(i)
    return lt


def perenos(text):
    string = re.sub(r'-\n', '', text)
    string = re.sub(r'\n', ' ', string)
    return string


# главная функция
def got_stat(data, f1, f2, vocabular):
    file1 = open(f1, 'w')
    file2 = open(f2, 'w')

    i = 1
    d = []
    dict_opechatki = []
    # for document in csv.reader(open(data, 'r'), delimiter='\t', quotechar='"'):

    for document in dataset_ktc(PATH + KTC):
        text = find_from_doc_rus(document)

        i = i + 1

        doc = perenos('\n'.join(text))

        doc_word = nltk.word_tokenize(doc.lower())
        print(doc)
        if len(doc_word) == 0:
            continue

        # нахождение опечаток и вероятности по ним
        mistake = find_punct_num_ss_eng(doc_word, vocabular)
        for miss in mistake:
            dict_opechatki.append(miss)

        ver = find_ver(doc_word, mistake)

        # формирование списка процентов опечаток
        d = list(np.append(ver, d))

    # колличество документов
    length_docs = length(i)

    # подсчет частоты встречаемости каждой опечатки в тексте
    frequency = count_frequency_of_opechatki(dict_opechatki)

    # формирование словаря dict{носмер документа: значение вероятности}
    dictionary_of_ver = dict(zip(length_docs, d))

    ''' сортировка по частоте встречаемости и сохранение опечаток, процента опечаток
        с указанием предела (начиная с какого процента печатать результат)'''

    sort_delete_save(frequency, file1, N)
    sort_delete_save_other_format(dictionary_of_ver, file2, M)


vocabulary_word = dictionary_words(PATH+MAIN_WORDS)
got_stat(PATH+DATA, PATH+SAVE_OPECHATKI, PATH+SAVE_VER, vocabulary_word)