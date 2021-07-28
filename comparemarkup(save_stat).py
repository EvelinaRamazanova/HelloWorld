import json
import pprint
from itertools import zip_longest as iz

DOCCANO_MAKEUP = '/home/evelina/Рабочий стол/stat/doccano.json'
AUTO_MAKEUP = '/home/evelina/Рабочий стол/stat/new_data.json'

FOLDER = '/home/evelina/Рабочий стол/stat/match/'


def read_annotated(path, indexes):
    doc_makeup_list = []
    with open(path, 'r') as database:
        for page in database.readlines():
            page = json.loads(page)
            for index in indexes:
                del page[index]

            doc_makeup_list.append(page)
    return doc_makeup_list


def save_format(text_attributes, file_to_save):
    for one_dict in [{k: v} for k, v in text_attributes.items()]:
        file_to_save.write((json.dumps(one_dict, ensure_ascii=False)) + '\n')


def main_fun():
    indexes_auto = ['number', 'meta', 'annotation_approver']
    indexes_doccano = ['number']

    auto = read_annotated(AUTO_MAKEUP, indexes_auto)
    doccano =read_annotated(DOCCANO_MAKEUP, indexes_doccano)

    full_auto_values = [[k for k in i.values()] for i in auto]
    full_doccano_values = [[k for k in i.values()] for i in doccano]

    true = 0
    false = 0
    full = 0

    d1 = {}
    d2 = {}
    d3 = {}
    d4 = {}

    with open(FOLDER+'all_match.txt', 'w') as all_match, \
            open(FOLDER+'first_match.txt', 'w') as first_match, \
            open(FOLDER+'second_match.txt', 'w') as second_match, \
            open(FOLDER+'no_one_match.txt', 'w') as no_one_match:

        for auto_val in full_auto_values:
            for docc_val in full_doccano_values:
                if auto_val[0] in docc_val[0]:  # если текст совпадает => имеется разметка на одинаковых страничках

                    ######################################################
                    if auto_val[1] == docc_val[1]:
                        # print('полностью совпавшая разметка: ', auto_val[1], ':', docc_val[1])
                        continue

                    # Сравнение меток из разметчика с метками из авторазметки
                    for i in docc_val[1]:
                        full = full+1

                        if i[0] in [j[0] for j in auto_val[1]] and i[1] in [j[1] for j in auto_val[1]]:
                            print('совпало оба знач-я: ', i)
                            true = true+1

                            d = {auto_val[0]: i}
                            for k, v in d.items():
                                d1.setdefault(k, []).append(v)
                            continue

                        elif i[0] in [j[0] for j in auto_val[1]]:
                            # print('неточность в конечном значении метки: ', i)
                            false = false+1

                            d = {auto_val[0]: i}
                            for k, v in d.items():
                                d2.setdefault(k, []).append(v)
                            continue

                        elif i[1] in [j[1] for j in auto_val[1]]:
                            # print('неточность в начальном значении метки: ', i)
                            false = false+1

                            d = {auto_val[0]: i}
                            for k, v in d.items():
                                d3.setdefault(k, []).append(v)
                            continue
                        else:
                            # print('знач-я имеющиеся в выгрузке, которых нет в авторазметке : ', i)
                            false = false+1

                            d = {auto_val[0]: i}
                            for k, v in d.items():
                                d4.setdefault(k, []).append(v)
                    ######################################################
                    # print('Авторазметка: {}\nВыгрузка: {}\n\n'.format(auto_val[1], docc_val[1]))

        save_format(d1, all_match)
        save_format(d2, first_match)
        save_format(d3, second_match)
        save_format(d4, no_one_match)

        stat_true = (true / full) * 100
        stat_false = (false / full) * 100
        print('True: {:.3f} %\nFalse: {:.3f} %\n'.format(stat_true, stat_false))


main_fun()