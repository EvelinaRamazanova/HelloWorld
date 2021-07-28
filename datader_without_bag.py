# -*- coding: utf8 -*-
import re
import json
import csv
import sys
import numpy as np
import os
import collections
import nltk
from collections import Counter

import pprint

csv.field_size_limit(sys.maxsize)
######################################################################

folder = '/Users/Evelina/Desktop/'

# Распарсенные логи МТС Банка в формате, приближенном к smarty
graylog = 'graylog_parsed.csv'

# кусочек данных, я сейчас посмотрю, получится ли попасть на сервер или нужны доступы, и остальной кусочек выгружу
# Эти данные можно у себя хранить, только их нельзя заливать в гитлаб и т.д.
state = '2020_01_2.csv'


######################################################################
# рекурсивное раскрытие вложенного словаря
def recursive_items(dictionary, prefix=''):
    for k, v in dictionary.items():

        # формат записи рекурсивных ключей + формирование нового словаря
        if isinstance(v, dict):
            for u in recursive_items(v, '{}{}_'.format(prefix, k)):
                yield u
        else:
            yield {'{}{}_'.format(prefix, k): v}


# парсер + формирование результата рекурсивного раскрытия вложенного словаря
def result_recursive(some_dict, word_for_catch):
    result = {}
    index_of_dict = some_dict.rfind(word_for_catch)  # подсчет начала словаря для парсера
    v2 = some_dict[index_of_dict:]  # удаляем слова до словаря и получаем чистый словарь
    print(v2)

    request = json.loads(re.sub(word_for_catch, '', v2))  # заменяем и переводим в json

    # парсим
    recursive = {}

    for items in recursive_items(request):
        recursive.update(items)

    # собираем все в 1 словарь
    result.update(recursive)
    result.update({'massage': some_dict[:index_of_dict] + word_for_catch})
    return result


# главная функция
def got_stat():

    check = 0

    # keys_list = set()
    # for line in csv.DictReader(open(folder + 'graylog_parsed.csv'), delimiter='|', lineterminator='\n'):
    #     for heading, info in line.items():
    #         if heading == 'nlp_class' and info != None:
    #             keys_list.add(info)

    keys_list = ['CardInfo', 'CreditCardMinPay',
                 'CreditCardDebt', 'CardBalance',
                 'VirtualCard', 'CardDetailing',
                 'Insurance', 'CanBotMoreHelp',
                 'Operator']

    d = {k: [] for k in keys_list}

    new_set = {}

    n = []
    for line in csv.DictReader(open(folder+'graylog-search-result-relative-0.csv')):
        for k, v in line.items():
            # if k in ['timestamp', 'source']:  # перезаписываем столбец timestamp и source
            #     new_set[k] = v
            # else:
                # столбец message

                # если в логах нет словаря => нечего парсить, записываем как есть
                # INFO [        ] - [JS-INFO] preprocess: targetState after nBest, "/start"

                for i in keys_list:
                    if i in v:

                        n.append(line)

    # with open(folder + 'graylog_3_0.csv', 'w') as f:
    #     csv_writer = csv.writer(f, delimiter='|')
    #     for i in n:
    #         csv_writer.writerow(i)


    # newlist = sorted(lst, key=lambda k: k['nlp_class'])
    with open(folder + 'graylog_3_0.csv', 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(n[0].keys())  # запись ключей словаря как название колонок
        for dict_item in n:  # заполнение колонок
            csv_writer.writerow(dict_item.values())


                # if '{' not in v:
                #     new_set[k] = v
                #
                # # если в логах есть словари, парсим
                # else:

                    # парсер + формирование результата рекурсивного раскрытия вложенного словаря

                    # if 'request:' in re.split(' ', v):
                    #     res = result_recursive(v, 'request:')
                    #     new_set.update(res)

                    # elif 'response:' in re.split(' ', v):
                    #     res = result_recursive(v, 'response:')
                    #     new_set.update(res)

                    #
                    # if 'END' in re.findall(r"[\w']+",  v):
                    #     result = {}
                    #     index_of_dict = v.rfind('END:')  # подсчет начала словаря для парсера
                    #     # if index_of_dict
                    #     v2 = v[index_of_dict+4:]  # удаляем слова до словаря и получаем чистый словарь
                    #
                    #     print( v2)
                    #     request = json.loads(v2)  # заменяем и переводим в json
                    #
                    #     print(request)
                        # парсим
                        # recursive = {}
                        #
                        # for items in recursive_items(request):
                        #     print(items)
                        #     recursive.update(items)
                        #
                        # # собираем все в 1 словарь
                        # result.update(recursive)
                        # result.update({'massage': some_dict[:index_of_dict] + word_for_catch})





                    # elif 'BEGIN:' in re.split(' ', v):
                    #     print(v)

                    # elif 'Response:' in re.split(' ', v) and '200' in re.split(' ', v):
                    #     print(v)
                    #     # v = v.replace('[', '{').replace(']', '}')
                    #     # print(v)
                    #     res = result_recursive(v, 'Response: 200')
                    #     new_set.update(res)
                        # print('@@@@@@@@@@@@@@@@@@@@', v)


                    # elif 'response:' in re.findall(r"[\w']+\(",  v):


                        # for i in (re.split(', ', v)):
                        #     print(i)
                        #     print()
                        # v = v.replace('(', '{').replace(')', '}').replace('=', ':')
                        # print(json.loads(v))
                        # res = result_recursive(v, 'BotResponse')
                        # print (res)
                        # print()



                        # result = {}
                        # index_of_dict = some_dict.rfind(word_for_catch)  # подсчет начала словаря для парсера
                        # v2 = some_dict[index_of_dict:]  # удаляем слова до словаря и получаем чистый словарь
                        # request = json.loads(re.sub(word_for_catch, '', v2))  # заменяем и переводим в json
                        #
                        # # парсим
                        # recursive = {}
                        #
                        # for items in recursive_items(request):
                        #     recursive.update(items)
                        #
                        # # собираем все в 1 словарь
                        # result.update(recursive)
                        # result.update({'massage': some_dict[:index_of_dict] + word_for_catch})

                    # else:
                    #     # print(v)
                    #     check += 1

    # print(check)  # 974 352 /853 565


                    # check += 1
                    # i = v.rfind('{')
                    # if i != 1:
                    #     v = v[i:]
                    # print(v)
                    # print()
                    #
                    # print(check)


                # for k in ['CardInfo', 'CreditCardMinPay',
                #           'CreditCardDebt', 'CardBalance',
                #                 'VirtualCard', 'CardDetailing',
                #                 'Insurance', 'CanBotMoreHelp',
                #                 'Operator']:
                #
                #     if k in re.split(' |,|:|{|}|\(|\)|"', v):
                #         d[k].append(k)
                #         print(line)
                #         print()

        # for heading, info in line.items():

            # if heading == 'nlp_class' and info != None:
            #     if info in d.keys():
            #         d[info].append(line)

    # d1 = {}
    # for k, v in d.items():
    #     if re.split('/', k)[-1] in ['CardInfo', 'CreditCardMinPay',
    #                                 'CreditCardDebt', 'CardBalance',
    #                                 'VirtualCard', 'CardDetailing',
    #                                 'Insurance', 'CanBotMoreHelp',
    #                                 'Operator']:
    #
    #         d1[re.split('/', k)[-1]] = len(v)

    # list_d = list(d.items())
    # list_d.sort(key=lambda i: i[1], reverse=True)
    # for i in list_d:
    #     print(i[0], ':', i[1])


got_stat()


##########################################################################################################
# разделение на классы без парсинга данных + статистика
def statistics():

    lst = []

    # формируем список ключей
    keys_list = []
    for line in csv.DictReader(open(folder + 'graylog_parsed.csv'), delimiter='|', lineterminator='\n'):
        for heading, info in line.items():
            if heading == 'nlp_class' and info is not None:

                if not re.findall('[a-z]', line['nlp_class'].split('/')[-1][0]) \
                        and line['nlp_class'] != '/start':
                    keys_list.append(line['nlp_class'])

    d = {k: [] for k in keys_list}  # для дальнейшего подсчета статистики

    # формируем датасет без лишних сценариев
    for line in csv.DictReader(open(folder + 'graylog_parsed.csv'), delimiter='|', lineterminator='\n'):
        for heading, info in line.items():
            if heading == 'nlp_class' and info is not None:

                if not re.findall('[a-z]', line['nlp_class'].split('/')[-1][0]) \
                     and line['nlp_class'] != '/start':
                    lst.append(line)

                    # for k, v in d.items():
                    #     if k == line['nlp_class']:
                    #         d[k].append(line)

    ##########################################################################################################
    # подсчет и сохранение статистики количества сценариев каждого лога
    # a = []
    # for k, v in d.items():
    #     a.append({'key': k, 'lengh': len(v)})

    # with open(folder + 'graylog.txt', 'w') as wrt:
    #     for i in sorted(a, key=lambda k: k['lengh'], reverse=True):
    #         print(i['key'], i['lengh'])
    #         wrt.write('{}: {}'.format(i['key'], i['lengh']) + '\n')
    ##########################################################################################################

    # print('Распределение готово')
    # print('Сортировка и сохранение результата')
    #
    # newlist = sorted(lst, key=lambda k: k['nlp_class'])
    # with open(folder + 'graylog_change.csv', 'w') as f:
    #     csv_writer = csv.writer(f, delimiter=',')
    #     csv_writer.writerow(newlist[0].keys())  # запись ключей словаря как название колонок
    #     for dict_item in newlist:  # заполнение колонок
    #         csv_writer.writerow(dict_item.values())


# statistics()


##########################################################################################################
def dbl():
    txt = set([line['question'] for line in csv.DictReader(
        open(folder + 'graylog_parsed.csv'), delimiter='|', lineterminator='\n')])

    d = {k: [] for k in txt}  # для дальнейшего подсчета статистики

    # формируем датасет без лишних сценариев
    for line in csv.DictReader(open(folder + 'graylog_parsed.csv'), delimiter='|', lineterminator='\n'):
        for k, v in d.items():
            if k == line['question']:
                d[k].append(line)

    full_length = []
    double_length = []

    new = []
    for k, v in d.items():

        full_length.append(len(v))
        # подсчет дублей
        if len(v) > 1:
            new.append(v[1])
            double_length.append(len(v))

    new_list = sorted(new, key=lambda k: k['id'])
    with open(folder + 'graylog_without_double.csv', 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(new_list[0].keys())  # запись ключей словаря как название колонок
        for dict_item in new_list:  # заполнение колонок
            csv_writer.writerow(dict_item.values())

    print('Среди', sum(full_length), sum(double_length), 'дублей\n', 'Процент дублированных документов:', (sum(double_length)/sum(full_length))*100)


# dbl();