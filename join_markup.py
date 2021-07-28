import json

PATH = '/Users/Evelina/Desktop/Выгрузки doccano/'
DATABASE = 'markup_2.json'


###############################################################################
# ПОДГОТОВКА ДАТАСЕТА К ОБЪЕДИНЕНИЮ МЕТКИ
def read_data(path):
    docs_lst = []
    names_lst = set()
    descriptions_lst = set()
    with open(path, 'r') as db:
        for doc in json.load(db):
            docs_lst.append(doc)
            names_lst.add(doc['name'])
            descriptions_lst.add(doc['description'])
    return list(names_lst), list(descriptions_lst), docs_lst


def new_data(names, descriptions, docs):

    names.sort()
    descriptions.sort()

    new_dict = {k: {v: [] for v in descriptions} for k in names}

    for k, v in new_dict.items():
        for doc in docs:
            if k == doc['name']:
                for val in v.keys():
                    if val == doc['description']:
                        part = {'id': doc['id'],
                                # 'description': doc['description'],
                                # 'text': doc['text'],
                                'label': doc['label']}
                        new_dict[k][val].append(part)
    yield new_dict


###############################################################################
names_list, descriptions_list, documents = read_data(PATH+DATABASE)
database = new_data(names_list, descriptions_list, documents)

# СОХРАНЕНИЕ ПОДГОТОВЛЕННОГО ДАТАСЕТА, ПОСЛЕ ЕГО СОРТИРОВКИ
full_set = []
for sets in database:
    for document in sets.values():
        for id_label in document.values():
            if not id_label:
                continue

            id_label_new = sorted(id_label, key=lambda x: x['id'])

            ku = []
            for labels_of_one_id in id_label_new:

                slovo = {'id': labels_of_one_id['id'], 'label': []}

                for label in labels_of_one_id['label'].split(';'):
                    markup = label.split(',')
                    offset = [int(markup[0]), int(markup[1]), markup[2]]
                    slovo['label'].append(offset)

                    # print('id: {}, {}'.format(labels_of_one_id['id'], offset))
                # print(slovo)
                ku.append(slovo)
            full_set.append(ku)

with open('/Users/Evelina/Desktop/' + 'nabor.json', 'w') as w:
    for i in full_set:
        print(i)
        w.write('%s\n' % json.dumps(i, ensure_ascii=False))
        # print('\n\n')
###############################################################################


#  СОЕДИНЕНИЕ РАЗМЕТКИ
def merge_labels():
    merge_data = []
    with open('/Users/Evelina/Desktop/nabor.json', 'r') as r:

        for reader in r.readlines():
            documents = json.loads(reader)

            doc = {'id': []}

            # чтение меток страниц документа
            markup_lst = []
            for page in documents:
                page['label'].sort(reverse=False)
                markup_lst.append(page['label'])

                # сохранение id страниц
                doc['id'].append(page['id'])

            # соединение меток, путем суммирования значений метки предыщущей страницы и последующей
            i = 0
            new = []  # полная разметка всех страниц документа
            while i+1 < len(markup_lst):

                # разметка страницы заканчивается markup_lst[i][-1] лэйбломб, конечное значение при этом markup_lst[i][
                # -1][1] складывается с разметкой следующей страницы markup_lst[i + 1]

                # суммируем конечное значение метки предыдущей страницы со всеми значениями лэйблов последующей страницы
                # сохраняем в новый список
                new_mark_lst = []
                for markup in markup_lst[i+1]:
                    # markup_lst[i][-1][1]+1 прибавляем 1 так как в дальнейшим при соединении текста добавится
                    # элемент '\n'.join
                    new_mark_lst.append([markup_lst[i][-1][1]+1 + markup[0],
                                         markup_lst[i][-1][1]+1 + markup[1],
                                         markup[2]])

                markup_lst[i+1] = new_mark_lst

                if i == 0:
                    new.append(markup_lst[i])
                new.append(markup_lst[i + 1])
                i += 1

            # доведение до нужного формата и сохранение в файл
            done = []
            for i in new:
                for j in i:
                    done.append(j)
            doc['label'] = done

            merge_data.append(doc)
    return merge_data

# merge_labels()


########################################################################################################################
# СОЕДИНЯМ ТЕКСТЫ ДОК-ОВ В СООБВЕТСТВИИ СО СКЛЕЕННОЙ РАЗМЕТКОЙ
def doccano_docs():
    d = []
    with open('/Users/Evelina/Desktop/Выгрузки doccano/markup_2.json', 'r') as db:
        for doc in json.load(db):
            d.append(doc)
    return d


def save_with_full_info():

    database = merge_labels()
    doccano = doccano_docs()

    with open('/Users/Evelina/Desktop/new_markup_2.json', 'w') as wrt:
        for json_doc in database:

            new = {}
            lst = list()

            id_lst = []
            for file in doccano:
                if file['id'] in json_doc['id']:
                    id_lst.append(file['id'])
                    new['name'] = file['name']
                    new['description'] = file['description']
                    lst.append(file['text'])

            new['id'] = id_lst
            new['text'] = '\n'.join(lst)
            new['label'] = json_doc['label']
            new['id'] = id_lst

            d = {'id': new['id'],
                 'name': new['name'],
                 'description': new['description'],
                 'text': new['text'],
                 'label': new['label']}

            print(d)
            wrt.write(json.dumps(d, ensure_ascii=False) + '\n')


save_with_full_info()


########################################################################################################################
def change_data_format():
    with open('/Users/Evelina/Desktop/Выгрузки doccano/markup_4.json', 'r') as r, \
            open('/Users/Evelina/Desktop/markup_4.json', 'w') as wrt:

        for doc_file in json.load(r):
            lab = []
            for label in doc_file['label'].split(';'):
                lab.append([int(label.split(', ')[0]), int(label.split(', ')[1]), label.split(', ')[2]])
            doc_file['label'] = lab
            wrt.write(json.dumps(doc_file, ensure_ascii=False) + '\n')


# change_data_format()
