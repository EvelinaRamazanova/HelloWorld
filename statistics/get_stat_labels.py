import json
import pprint
import datetime
from operator import itemgetter

FOLDER = '/Users/Evelina/Desktop/'


def read_data(path):

    check_doc = 0
    check_doc_with_dubl = 0
    with open(path+'markup_2.json', 'r') as f, open(path + 'stat_dubl_3.json', 'w') as w:
        for doc in json.load(f):
            print(doc)
            check_doc += 1

            doc_labels = doc['label']  # все метки одного документа

            new_dict = {'id': doc['id'],
                        'name': doc['name'],
                        'description': doc['description'],
                        'text': doc['text'],
                        # 'difference_label': [],
                        'new_label': []}

            int_labels = [[int(part.split(',')[0]), int(part.split(',')[1]),
                           part.split(',')[2]] for part in doc_labels.split('; ')]
            int_labels.sort(key=itemgetter(0, 1))


            # len(int_labels) - колличество меток в рамках одного документа
            for index in range(0, len(int_labels)):

                if index+1 < len(int_labels):

                    i = int_labels[index]
                    j = int_labels[index+1]

                    left = range(i[0], i[1])
                    right = range(j[0], j[1])
                    list_left = set(left)
                    a = list_left.intersection(right)

                    if a == set():  # если нет пересечений
                        # new_dict['new_label'].append([i[0], i[1], i[2]])
                        continue

                    dif = {'1. этот label': i, '2. пересекается с': j}
                    new_dict['new_label'].append(dif)

            if new_dict['new_label'] == []:
                continue

            check_doc_with_dubl += 1

            # pprint.pprint(new_dict)
            w.write('%s\n' % json.dumps(new_dict, ensure_ascii=False))
            print(new_dict)
    print(check_doc_with_dubl, 'документов из ', check_doc, 'имеют дубликаты')


read_data(FOLDER)