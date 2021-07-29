import json
from pprint import pprint
from operator import itemgetter

FILE = 'annotator_name.json'
FOLDER = '/Users/Evelina/Desktop/'
GROUPS_FILE = 'groups_dataset_3.json'


def join_attributes(file: str):
    """
    Объединение атрибут сущностей и сохранение списка значений от ключей id, text, labels
    :param file: data
    :return:
    """
    attributes_list = ['start_offset', 'end_offset', 'label', 'start_offset', 'end_offset']

    with open(file, 'r') as f:
        print()
        for line in json.load(f):

            attributes = [v for k, v in line.items() if k in attributes_list]
            print(line['id'], attributes)

            attributes = [attributes[1], attributes[0], attributes[2]]
            stat = {'id': line['id'],
                    'text': line['text'],

                    'labels': attributes,

                    'name': line['name'],
                    'description': line['description']}

            yield [stat for stat in stat.values()]


def get_groups(folder, file):
    """
    Сортировка списка значений ключей id, text, labels по текстку.
    Группировка сущностей по тексту. Добавление name и description.
    :return:
    """
    data_entity = [i for i in join_attributes(folder + file)]

    # сортировка по тексту
    sort_data = {}
    for doc_id, text, labels, name, description in sorted(data_entity, key=itemgetter(1)):
        sort_data.setdefault(text, []).append(labels)

    # группировка сущностей по тексту
    groups = {}
    for k, v in sort_data.items():
        for list_entity in data_entity:

            if list_entity[1] == k:

                groups['id'] = list_entity[0]
                groups['name'] = list_entity[3]
                groups['description'] = list_entity[4]
                # groups['user_id'] = list_entity[3]
                groups['text'] = k
                groups['labels'] = v

        yield groups


def save_data():
    """
    Сохранение
    :return:
    """

    groups_data = get_groups(FOLDER, FILE)
    with open(FOLDER + GROUPS_FILE, 'w', encoding='utf-8') as w:
        for item in groups_data:
            # pprint(item)
            w.write('%s\n' % json.dumps(item, ensure_ascii=False))


save_data()