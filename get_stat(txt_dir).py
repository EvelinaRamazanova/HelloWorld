# -*- coding: utf8 -*-
import re
import json
import csv
import sys
import numpy as np
import os
import nltk

csv.field_size_limit(sys.maxsize)

PATH = '/Users/Evelina/Desktop/'
DATA = 'data_search_typos/docs/'

MAIN_WORDS = 'data_search_typos/dict_full.txt'

SAVE_OPECHATKI = 'data_search_typos/save_opechatki.txt'
SAVE_VER = 'data_search_typos/save_ver.txt'

PUNCTUATION = set('!₽•≤€"ø#$%№&(‘)’,‚*+,-./©``:;<=>?@[\]—^_`{|}~”°›||‹„“«»®')


# смотреть опечатки которые повторяются в документах больше N раз
N = 20
# смотреть процент опечаток ниже M
M = 10


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

    kk = []
    vv = []
    f = {k: v for k, v in dict_for_sort.items() if v < n}

    save_name = open('/Users/Evelina/Desktop/filter_doc.txt', 'w', encoding='utf-8')
    for k, v in sorted(f.items(), key=lambda x: x[1], reverse=True):
        file.write('Документ № {}, процент опечаток: {:.3f}%\n'.format(k, v))
        save_name.write(k + '\n')

        kk.append(k)
        vv.append(v)

    d = dict(zip(kk, vv))

    # with open('/Users/Evelina/Desktop/mistakes_ver_from_doc.csv', 'w', newline='', encoding='utf-8') as file:
    #     for key in d.keys():
    #         print()
    #         file.write("{}, {:3f}\n".format(key, d[key]))


def perenos(text):
    string = re.sub(r'-\n', '', text)
    string = re.sub(r'\n', ' ', string)
    return string


# главная функция
def got_stat(path, f1, f2, vocabular):
    file1 = open(f1, 'w')
    file2 = open(f2, 'w')

    d = []
    dict_opechatki = []
    filename = []

    # в папке находим pdf файлы
    os.chdir(path)
    for txt_file in os.listdir(path):
        if txt_file.endswith(".txt"):
            f = open(txt_file, 'r')

            text = f.read()

            doc = perenos(text)

            # токены одного документа
            doc_word = nltk.word_tokenize(doc.lower())

            # нахождение опечаток и вероятности по ним в рамках одного документа
            mistake = find_punct_num_ss_eng(doc_word, vocabular)

            ver = find_ver(doc_word, mistake)

            # сохранем опечатки со всех док-ов
            for miss in mistake:
                dict_opechatki.append(miss)

            # формирование списка процентов опечаток
            d = list(np.append(ver, d))

        filename.append(txt_file)

    # подсчет частоты встречаемости каждой опечатки в тексте
    frequency = count_frequency_of_opechatki(dict_opechatki)

    # формирование словаря dict{носмер документа: значение вероятности}
    dictionary_of_ver = dict(zip(filename, d))

    ''' сортировка по частоте встречаемости и сохранение опечаток, процента опечаток
        с указанием предела (начиная с какого процента печатать результат)'''

    sort_delete_save(frequency, file1, N)
    sort_delete_save_other_format(dictionary_of_ver, file2, M)


vocabulary_word = dictionary_words(PATH+MAIN_WORDS)
got_stat(PATH+DATA, PATH+SAVE_OPECHATKI, PATH+SAVE_VER, vocabulary_word)