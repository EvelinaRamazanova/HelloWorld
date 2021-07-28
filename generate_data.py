import csv
import sys
import json
import pprint

csv.field_size_limit(sys.maxsize)

#############################################################################################
PART_OF_DATA = 'full_data_3.json'
FULL_DATA = 'full_data_3.json'

PATH = '/Users/Evelina/Desktop/table_doccano/'
T1 = 'database/SELECT_t___FROM_public_api_document_t.csv'
T2 = 'database/SELECT_t___FROM_public_api_project_t.csv'
T3 = 'database/SELECT_t___FROM_public_api_sequenceannot.csv'
T4 = 'database/SELECT_t___FROM_public_api_label_t.tsv'
#############################################################################################


def sort_tab_2(folder: str,
               table2: str):
    """
    Выделение наборов относящихся только к нужной выборке по таблице api_project.
    :param folder: path to folder
    :param table2: tables name
    :return:
    """

    with open(folder + table2, 'r') as api_project:
        for line_from_tab2 in csv.reader(api_project, delimiter='\t', quotechar='"'):

            # смотрим по названию набора в таблице 2
            if 'Набор 1.' in ' '.join(line_from_tab2):
                dict_tab = {'project_id': line_from_tab2[0],
                            'name': line_from_tab2[1],
                            'description': line_from_tab2[2]}

                yield dict_tab


def sort_tab_1(folder: str,
               table1: str,
               table2: str):
    """
    Просмотр совпадающих id проектов из талибы api_document и api_project.
    :param folder: path to folder
    :param table1: first tables name
    :param table2: tables name
    :return:
    """

    dict_list = []
    with open(folder + table1, 'r') as api_document:
        for line_from_tab1 in csv.reader(api_document, delimiter='\t', quotechar='"'):

            # если совпали id проектов из талибы api_document и api_project
            for dict_tab in sort_tab_2(folder, table2):

                if line_from_tab1[5] == dict_tab['project_id']:
                    dict_tab.update({'doc_id': line_from_tab1[0],
                                     'text': line_from_tab1[1]})
                    # print(dict_tab)
                    if dict_tab not in dict_list:
                        dict_list.append(dict_tab)
    return dict_list


def sort_tab_3(folder: str,
               table1: str,
               table2: str,
               table3: str):
    """
    Просмотр совпадающих id документов из талибы api_document и api_sequence_annotation.
    :param folder: path to folder
    :param table1: first tables name
    :param table2: tables name
    :param table3: tables name
    :return:
    """
    tab_12 = sort_tab_1(folder, table1, table2)

    with open(folder + table3, 'r') as api_sequence_annotation, open(folder + PART_OF_DATA, 'w') as w:
        for line_from_tab3 in csv.reader(api_sequence_annotation, delimiter='\t', quotechar='"'):

            # если совпали id документов из талибы api_document и api_sequence_annotation
            for dict_tab in tab_12:
                if line_from_tab3[7] == dict_tab['doc_id'] and line_from_tab3[9] != '1':

                    dict_tab_123 = {
                        'doc_id': dict_tab['doc_id'],
                        'name': dict_tab['name'],
                        'description': dict_tab['description'],
                        'text': dict_tab['text'],

                        # 'user_id': line_from_tab3[9],
                        'label_id': line_from_tab3[8],
                        'start_offset': line_from_tab3[5],
                        'end_offset': line_from_tab3[6],
                        'created_at': line_from_tab3[3],
                        'updated_at': line_from_tab3[4]
                    }

                    print(dict_tab_123)
                    w.write(json.dumps(dict_tab_123, ensure_ascii=False) + '\n')


def sort_tab_4(folder: str,
               table4: str):
    """
    Просмотр совпадающих id меток из талибы api_sequence_annotation и api_label
    :param folder: path to folder
    :param table4: tables name
    :return:
    """
    tab_123 = []
    with open(folder + PART_OF_DATA, 'r') as r:
        for line in r.readlines():
            print(line)
            tab_123.append(json.loads(line))

    i = 0
    with open(folder + table4, 'r') as api_label, open(folder + FULL_DATA, 'w') as wrt:
        for line_from_tab4 in csv.reader(api_label, delimiter='\t', quotechar='"'):
            for doc in tab_123:
                if doc['label_id'] == line_from_tab4[0]:
                    doc['label'] = line_from_tab4[1]
                    doc['start_label'] = line_from_tab4[6]
                    doc['end_label'] = line_from_tab4[7]
                    i += 1
                    wrt.write(json.dumps(doc, ensure_ascii=False) + '\n')
    print(i)


# sort_tab_1(folder=PATH, table1=T1, table2=T2)
# sort_tab_2(folder=PATH, table2=T2)
sort_tab_3(folder=PATH, table1=T1, table2=T2, table3=T3)
sort_tab_4(folder=PATH, table4=T4)