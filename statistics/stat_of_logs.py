# -*- coding: utf8 -*-
import re
import json
import csv
import sys
import numpy as np
import os
import nltk

csv.field_size_limit(sys.maxsize)


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
        if word in punctuation:
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


# главная функция
def got_stat(path_to_data, vocabular):

    sum_ver = []
    check = 0
    for line in csv.DictReader(open(path_to_data), delimiter='|', lineterminator='\n'):
        check += 1
        question = line['question']
        if question is not None:

            # токены одного сценария
            words = nltk.word_tokenize(question.lower())

            # нахождение опечаток и вероятности по ним в рамках одного сценария
            mistake = find_punct_num_ss_eng(words, vocabular)
            ver = find_ver(words, mistake)

            sum_ver.append(ver)

    print('Всего текстов: ', check,
          '\nТекстов с опечатками:', len(sum_ver),
          '\nПроцент ломанных текстов:',
          (len(sum_ver)/sum(sum_ver))*100, '%')


folder = '/Users/Evelina/Desktop/'
graylog = 'graylog-search-result-relative-0.csv'

# Распарсенные логи МТС Банка в формате, приближенном к smarty
graylog_parsed = 'graylog_parsed.csv'

dictionary = 'doccano/dict_full.txt'
punctuation = set('!₽•≤€"ø#$%№&(‘)’,‚*+,-./©``:;<=>?@[\]—^_`{|}~”°›||‹„“«»®')

vocabulary_word = dictionary_words(folder+dictionary)
got_stat(folder+graylog_parsed, vocabulary_word)

