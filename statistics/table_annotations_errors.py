import json
import csv
import re
from nltk.tokenize import wordpunct_tokenize

PATH = '/Users/Evelina/Desktop/'

""" Из словаря error.txt сделать табличку вида (например, xlsx + csv) - | Некорректный(е) символ(ы) | 
Корректный(е) символ(ы) | Суммарное количество раз частотности | Сумма цифр | Вероятность 
(суммарное кол-во раз / сумму цифр в словаре) |
Некорректный(е) символ(ы) - это сама ошибка (только в виде одного или нескольких символов), чтобы можно было прямо 
Python-словарь сделать
Корректный(е) символ(ы) - это корректная замена
Суммарное количество раз частотности (это из скобочек) - сумма всех цифр в скобках для пар слов из словаря, 
в которых есть эта ошибка
Сумма цифр из всех скобочек в словаре - полная сумма цифр, типа все ошибки в словаре, их частотность
Вероятность - тут одно просто делим на другое """


def find_errors_letter():
    errors = []
    with open(PATH+'error.txt', 'r', newline='\n') as data:
        for line in data.readlines():
            error = re.sub('\n', '', line).split(' ')

            if len(error) > 4: continue
            if len(error[0]) != len(error[2]): continue

            letters = {'Исходные данные': ''.join(error),
                       'Некорректный(е) символ(ы)': [],
                       'Корректный(е) символ(ы)': []}

            error_word = error[0]
            correct_word = error[2]

            i = 0
            for token_error in error_word:
                i += 1
                j = 0
                for correct in correct_word:
                    j += 1
                    if i == j:
                        if token_error != correct:
                            letters['Некорректный(е) символ(ы)'].append(token_error)
                            letters['Корректный(е) символ(ы)'].append(correct)

            letters['Check'] = wordpunct_tokenize(error[3])[1]

            if letters['Некорректный(е) символ(ы)'] == []: continue
            if letters['Некорректный(е) символ(ы)'] == ['с', 'л', 'о', 'в', 'и']: continue
            if letters['Некорректный(е) символ(ы)'] == ['о', 'д', 'р', 'я', 'д', 'ч', 'и', 'к', 'о', 'м']: continue

            errors.append(letters)
    return errors


def list_sum(num_list):
    the_sum = 0
    for i in num_list:
        the_sum = the_sum + i
    return the_sum


def lst_errors():
    dict_letters = find_errors_letter()  # словарь корректных и некорректных слов
    lst_letters = []  # список букв - опечаток
    for line in dict_letters:
        test = [line['Некорректный(е) символ(ы)'], line['Корректный(е) символ(ы)']]
        if test not in lst_letters:
            lst_letters.append(test)
    return lst_letters


def check_error():
    letters = find_errors_letter()
    lst_letters = lst_errors()

    d = {}
    for point in lst_letters:
        d['Некорректный(е) символ(ы)'] = point[0]
        d['Корректный(е) символ(ы)'] = point[1]

        lst = []
        for symbol in letters:
            if symbol['Некорректный(е) символ(ы)'] == d['Некорректный(е) символ(ы)'] and \
                    symbol['Корректный(е) символ(ы)'] == d['Корректный(е) символ(ы)']:
                lst.append(int(symbol['Check']))
        d['Суммарное количество раз частотности'] = list_sum(lst)
        yield d


def summa():
    data = check_error()
    num = []
    for line in data:
        num.append(line['Суммарное количество раз частотности'])
    return list_sum(num)


def dataset():
    for i in check_error():
        i['Сумма цифр'] = summa()
        i['Некорректный(е) символ(ы)'] = ', '.join(i['Некорректный(е) символ(ы)'])
        i['Корректный(е) символ(ы)'] = ', '.join(i['Корректный(е) символ(ы)'])
        i['Вероятность'] = i['Суммарное количество раз частотности']/i['Сумма цифр']
        yield i


with open(PATH+'letters_stat.csv', 'w', newline="") as wrt:
    columns = ['Некорректный(е) символ(ы)',
               'Корректный(е) символ(ы)',
               'Суммарное количество раз частотности',
               'Сумма цифр', 'Вероятность']

    writer = csv.DictWriter(wrt, fieldnames=columns)
    writer.writeheader()
    writer.writerows(dataset())