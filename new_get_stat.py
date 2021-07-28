# -*- coding: utf8 -*-
import re
import json
import csv
import sys
import numpy as np
import nltk
from nltk.tokenize import wordpunct_tokenize
from tqdm import tqdm
import os

csv.field_size_limit(sys.maxsize)

PATH = '/Users/Evelina/Desktop/'
KTC = 'database_ktc.csv'

MAIN_WORDS = 'data_search_typos/opcorpora.txt'

SAVE_OPECHATKI = 'data_search_typos/save_opechatki.txt'
SAVE_VER = 'data_search_typos/save_ver.txt'

PUNCTUATION = set('!"#$%│•…№&\'(‘)’,‚*■+,-./©``:\|;<=>?@[\]—^_`{|}~”°›‹„“«»®')

# смотреть опечатки которые повторяются в документах больше N раз
N = 0
# смотреть процент опечаток выше M
M = 0


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


#########################################################################
# чтение датасета размеченных документов с ктс без приложений
def read_markup():
    folder = PATH + '/Выгрузки doccano/'
    for file in os.listdir(folder):
        if file.endswith('.json'):
            with open(folder + file, 'r') as reader:
                for doc in reader.readlines():
                    doc = json.loads(doc)
                    # print(doc['text']])
                    yield doc['text']


# чтение датасета с ктс
def dataset_ktc(path):
    with open(path, 'r') as ktc:
        for doc in csv.reader(ktc):

            if doc[2] == 'NULL':
                continue
            doc = json.loads(doc[2])
            lst = list()
            for values in doc.values():
                for blocks in values['blocks'].values():
                    lst.append(blocks['content']['rus'])
            yield '\n'.join(lst)
#########################################################################


def perenos(text):
    string = re.sub(r'-\n', '', text)
    string = re.sub(r'\n', ' ', string)
    return string


# нахождение знаков пунктуации, цифр, английких и словарных слов в документах
def find_punct_num_ss_eng(text, dict_annotation):
    mistake = []
    i = 0

    with open(PATH + 'test_file.txt', 'a') as test:
        for word in text:

            i += 1

            if word in PUNCTUATION:
                continue
            elif word in re.findall(r'^\d+$', word):
                continue
            elif word in re.findall(r'[a-zA-Z]+', word):
                continue
            elif word in dict_annotation:
                continue
            else:

                if word in re.findall('№.+|\w.|\w.\d|\d+.\d+.|\w', word):
                    continue

                elif word in re.findall('\d+.\d+.\d+.|\d.+\d.+\d.+|\d.\d+|\d.\d+.|\d{4}.|.+\d{4}.+', word):
                    continue

                elif word in re.findall('\d+.\d+.\d+.+|\d+.\d+|\d.\d.|\d.\d.$|\d.\d.\d$|\d+.\w+.\d+', word):
                    continue

                elif word in re.findall('\w$|\w.\w', word):
                    continue

                else:
                    punct_lst = set()
                    for tok in word:
                        if tok in PUNCTUATION:
                            punct_lst.add(''.join(word))

                    if word in punct_lst:
                        continue

                    # try:
                    #     print('error word:', text[i-1])
                    #     print('error line:', ' '.join([text[i-10], text[i-1].upper(), text[i+10]]), '\n\n')
                    #     test.write(' {} ({}) {}\n'.format(text[i-10], text[i-1], text[i+10]))
                    #
                    # except IndexError:
                    #     print('some error out of the string:', text[i-1])

                    test.write(word + '\n')
                    mistake.append(word)

    return mistake


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


# главная функция
def got_stat(f1, f2, vocabular):
    file1 = open(f1, 'w')
    file2 = open(f2, 'w')

    check_documents = 0

    percent_lst = []
    opechatki_lst = []

    # dataset = dataset_ktc(PATH + KTC)
    dataset = read_markup()

    for document in tqdm(dataset):
        doc = perenos(document)
        docs_word = wordpunct_tokenize(doc.lower())

        if len(docs_word) == 0:
            continue

        # нахождение опечаток и вероятности по ним
        mistake = find_punct_num_ss_eng(docs_word, vocabular)  # опечатки одного документа
        for miss in mistake:
            opechatki_lst.append(miss)

        # вычисление вероятности появления опечаток (в каком документе больше всего ошибок)
        percent_errors = (len(mistake) / len(docs_word)) * 100

        # формирование списка процентов опечаток
        percent_lst = list(np.append(percent_errors, percent_lst))

        # колличество документов
        check_documents += 1

    # список номеров документов
    lst_num_docs = length(check_documents)

    # подсчет частоты встречаемости каждой опечатки, относительно всех опечаток
    frequency = count_frequency_of_opechatki(opechatki_lst)

    # формирование словаря dict{носмер документа: значение вероятности}
    dictionary_of_ver = dict(zip(lst_num_docs, percent_lst))

    ''' сортировка по частоте встречаемости и сохранение опечаток, процента опечаток
        с указанием предела (начиная с какого процента печатать результат)'''

    sort_delete_save(frequency, file1, N)
    sort_delete_save_other_format(dictionary_of_ver, file2, M)


vocabulary_word = dictionary_words(PATH + MAIN_WORDS)
got_stat(PATH + SAVE_OPECHATKI, PATH + SAVE_VER, vocabulary_word)