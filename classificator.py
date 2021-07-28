# -*- coding: utf8 -*-
import csv
import sys
import nltk
import json
import pprint

csv.field_size_limit(sys.maxsize)


# чтение строки файла словаря
def dictionary_words(path):
    file = open(path, 'r').read().split('\n')
    dictionary = set([line.lower() for line in file])
    ln = len(dictionary)
    print('Сформировал словарь (Длина словаря: {})'.format(ln))
    return dictionary


# чтение датасета
def read_dataset(path):
    return [doc for doc in csv.reader(open(path, 'r'))]


def main_fun(dicts_path, datasets_path, saved_path):

    dict_list = dictionary_words(dicts_path)
    data_list = read_dataset(datasets_path)

    i = 0

    # подсчет распределенных пунктов
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0
    count_6 = 0
    count_7 = 0
    count_8 = 0

    keys_list = {'Оплата аванса',
                 'Ежемесячная/ежегодная оплата',
                 'Полная оплата работ (постфактум)',
                 'Предоплата с последующим повышением',

                 # 'Частичная оплата',
                 # 'Полная предоплата по договору',

                 'Оплата штрафов и неустоек',
                 'Обязанности исполнителя',
                 'Прочие условия',
                 'Расторжение заказа',
                 'Другое/Не подходит ни в одну из категорий'
                 }

    result = {key: [] for key in keys_list}
    for punkt in data_list:
        for podpunkt in punkt:

            i += 1

            tokens = nltk.word_tokenize(podpunkt)

            count_dict_words = 0
            for word in tokens:
                if word in dict_list:
                    count_dict_words += 1

            try:
                stat = (count_dict_words/len(tokens)) * 100
            except ZeroDivisionError:
                continue

            # условия отсеивания
            if len(tokens) < 30:
                continue

            if stat > 30:

                ############################################################
                if 'аванс' in podpunkt.lower():
                    result['Оплата аванса'].append(podpunkt)
                    count_1 += 1

                elif 'в месяц' in podpunkt.lower() or \
                        'в год' in podpunkt.lower():
                    result['Ежемесячная/ежегодная оплата'].append(podpunkt)
                    count_2 += 1

                elif 'штраф' in podpunkt.lower() or \
                        'неустойк' in podpunkt.lower():
                    result['Оплата штрафов и неустоек'].append(podpunkt)
                    count_3 += 1

                elif 'общая стоимость' in podpunkt.lower() or \
                        'общая цена ' in podpunkt.lower() or \
                        'общая сумма' in podpunkt.lower() or \
                        'стоимость работ' in podpunkt.lower() or \
                        'СТОИМОСТЬ' in podpunkt:
                    result['Полная оплата работ (постфактум)'].append(podpunkt)
                    count_4 += 1

                elif 'предварительная стоимость' in podpunkt.lower():
                    result['Предоплата с последующим повышением'].append(podpunkt)
                    count_5 += 1

                elif 'прочие условия' in podpunkt.lower():
                    result['Прочие условия'].append(podpunkt)
                    count_6 += 1

                elif 'обязанности' in podpunkt.lower():
                    result['Обязанности исполнителя'].append(podpunkt)
                    count_7 += 1

                elif 'расторгнуть подписанный' in podpunkt.lower():
                    result['Расторжение заказа'].append(podpunkt)
                    count_8 += 1

                else:
                    result['Другое/Не подходит ни в одну из категорий'].append(podpunkt)

                ############################################################

    print('Общее число документов: ', i, '\n',
          'Оплата аванса: ', count_1, '\n',
          'Ежемесячная/ежегодная оплата: ', count_2, '\n',
          'Полная оплата работ (постфактум): ', count_3, '\n',
          'Предоплата с последующим повышение: ', count_4, '\n'
          'Оплата штрафов и неустоек: ', count_5, '\n',
          'Обязанности исполнителя: ', count_6, '\n',
          'Прочие условия: ', count_7, '\n',
          'Расторжение заказа: ', count_8, '\n')

    # отберем по N док-ов из каждого класса
    # d1 = {}
    # for k, v in result.items():
    #     if len(v) > 25:
    #         d1[k] = v[0:25]
    #     else:
    #         d1[k] = v

    with open(saved_path, 'w') as file:
        file.write(json.dumps(result, ensure_ascii=False))


PATH = '/Users/Evelina/Desktop/'
DATA = 'output1.csv'
NEW_DATA = 'content.csv'
DICT_WORDS = 'doccano/dict_full.txt'

main_fun(dicts_path=PATH + DICT_WORDS,
         datasets_path=PATH + DATA,
         saved_path=PATH+'oplata_sort_full.json')


