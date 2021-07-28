# -*- coding: utf8 -*-
import re
import string
import json
import csv
import sys
import glob
import os
import numpy as np
import os.path

import shutil

csv.field_size_limit(sys.maxsize)
DATA = '/home/evelina/Рабочий стол/for_annotation.csv'
PATH = '/home/evelina/Рабочий стол/json/'

# номер документа
N = 15


# создание папки для сохранения файла
def gen_dir(path, n):
    all_page = page_read()
    s = length(all_page)
    # os.makedirs(path + 'Док-т № {} ({} стр.)'.format(n, s))
    p = path + 'Док-т № {} ({} стр.)/'.format(n, s)
    return p


# удалениие файлов в папке
def del_file_in_dir(path):
    os.chdir(path)
    files = glob.glob('*.json')
    for filename in files:
        os.unlink(filename)


# чтение csv и нахождение определенного документа по номеру n
def csv_reader(data, n):
    read_data = open(data, 'r')
    reader = csv.reader(read_data, delimiter=',')
    docs = [doc for doc in reader]
    doc = docs[n]
    return doc


# список текстов всех страниц документа
def page_read():
    doc = csv_reader(DATA, N)
    str_doc = ''.join(doc)
    json_doc = json.loads(str_doc)

    all_page = []
    for k, v in json_doc.items():
        lst = list()
        for k1, v1 in v['blocks'].items():
           lst.append(v1['content']['rus'])
        d = {'text': '\n\n'.join(lst)}
        all_page.append(d)

        print('Стр. № {}: {}'.format(k, d))
    return all_page


# колличество страниц
def length(file):
    ln = len(file)
    return ln


# сохранение в .json
def save_page_in_dir(path, all_page):
    ln = length(all_page)
    for i in range(1, ln):
        file_name = path + 'стр. {}.json'.format(i)
        with open(file_name, 'w') as output:
            for page in all_page:
                output.write(json.dumps(page, ensure_ascii=False))


# общая функция
def main_function(p, n):
    # объявление пути
    path = gen_dir(p, n)

    # очищение папки от файлов
    del_file_in_dir(path)

    # список текстов всех страниц документа
    all_page = page_read()

    # сохранение в .json
    save_page_in_dir(path,  all_page)


main_function(PATH, N)