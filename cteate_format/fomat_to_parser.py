import csv
import sys
import json
import re
import nltk

csv.field_size_limit(sys.maxsize)


# чтение строки файла словаря
def dictionary_words(path):
    dictionary = set([line.lower() for line in open(path, 'r').read().split('\n')])
    print('Сформировал словарь (Длина словаря: {})'.format(len(dictionary)))
    return dictionary


def open_data(path):
    return [i[1] for i in csv.reader(open(path, 'r'), delimiter='\t')]


# извлечение текста из json
def txt_from_doc(document):
    lst = list()
    for val in json.loads(document).values():
        try:
            for block in val['blocks'].values():
                txt = re.sub('^"', '', block['text'])
                txt = re.sub('"$', '', txt)
                lst.append(txt)
        except KeyError:
            continue
    return lst


# удаление приложения
def delete_annex(document):
    txt_without_annex = []
    for line in document:
        if not re.search('^приложение № 1$', line.lower()) or \
                not re.search('^приложение №1$', line.lower()):
            txt_without_annex.append(line)
        else:
            break
    return txt_without_annex


def perenos(text):
    string = re.sub(r'-\n', '', text)
    string = re.sub(r'\n', ' ', string)
    return string


# проверяем процент чистоты текста
def stat_ver(text, dictionary, n):

    tokens = nltk.word_tokenize(text)
    tokens_from_dict = [word for word in tokens if word.lower() in dictionary]
    blank_paper = {}
    if len(tokens) != 0 and len(tokens_from_dict) != 0:

        # пропускать документы с процентом опечаток выше n
        if (len(tokens_from_dict) / len(tokens)) * 100 > n:
            blank_paper['text'] = text

    if blank_paper != {}:
        return blank_paper


def writer_file(path, documents):
    with open(path, 'w') as wrt:
        for doc in documents:
            wrt.write(json.dumps(doc, ensure_ascii=False) + '\n')


def main():
    opencorpora = '/Users/Evelina/Desktop/opencorpora.txt'
    path_to_db = '/Users/Evelina/Desktop/content_27.04.2020.tsv'
    path_to_new_db = '/Users/Evelina/Desktop/content.json'

    dict_words = dictionary_words(path=opencorpora)
    database = open_data(path=path_to_db)

    db = []
    for file in database:
        if not file:
            continue

        txt = txt_from_doc(document=file)
        print('извлечение текста из json')

        txt_without_annex = delete_annex(document=txt)
        print('удаление приложения')

        txt_list = '\n'.join(txt_without_annex)

        # txt_list = perenos(text='\n'.join(txt_without_annex))
        # print('перенос')

        result = stat_ver(text=txt_list, dictionary=dict_words, n=50)
        print('Удалены документы с процентов нижу 50')

        if result not in db:
            db.append(result)

    writer_file(path=path_to_new_db, documents=db)


# main()

def read_():
    data = [json.loads(doc) for doc in (open('/Users/Evelina/Desktop/content.json', 'r')).readlines()]

    path_to_new_db = '/Users/Evelina/Desktop/1/content_9.json'

    db = data[000:1000]

    i = 0
    for k in db:
        i += 1
    print(i)

    writer_file(path=path_to_new_db, documents=db)


read_()