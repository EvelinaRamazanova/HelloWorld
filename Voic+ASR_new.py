import os
import json
import pprint


def research_txt(path):
    """
    Найти тексты и папки в которых они находятся

    :param path - путь до директории nov
    :return:
    """

    for folders, sub_dirs, files in os.walk(path, topdown=False):
        if folders.startswith('/Users/Evelina/Desktop/nov/данные с отекстовками/'):
            for file in files:

                if file.endswith('.txt'):
                    for txt in open(folders+'/'+file, 'r').readlines():

                        result = {
                            'folder': folders.split('/')[-1],  # номер папки в которой лежит отекстовки
                            'file_name': file,                 # название файла
                            'text': txt                        # отекстовка
                                }

                        yield result


def find_file(path):
    """
    Поиск json фойлов

    :param path - путь до директории nov
    :return:
    """

    result_with_txt = []
    result_no_txt = []
    for folders, sub_dirs, files in os.walk(path + '/' + 'json/', topdown=False):

        for file in files:

            if file.startswith('no_text'):
                json_no_txt = json.load(open(os.path.join(folders, file), 'r'))  # json одной папки без отекстовок
                first = {folders.split('/')[-1]: json_no_txt}
                result_no_txt.append(first)

            elif file.startswith('with_text'):
                json_txt = json.load(open(os.path.join(folders, file), 'r'))  # json одной папки с отекстовками
                second = {folders.split('/')[-1]: json_txt}
                result_with_txt.append(second)

    return result_with_txt, result_no_txt


def fun(path):
    """
    Общая функция склейки json-а

    :param path: путь до папки nov
    :return:
    """

    # спислок словарей в виде {номер папки в которой находится json:json-ы}
    result_with_txt, result_no_txt = find_file(path)

    # новые текстовики которые надо перенести в соответствующие json-ы
    # содержат номер папки в которой лежит отекстовки, название файла, отекстовки
    folder_and_json = research_txt(path=Desktop+PATH)

    new = {}  # склеинный json
    for with_txt in result_with_txt:

        for no_txt in result_no_txt:

            for txt in folder_and_json:  # находим отекстовки, чтобы дополнить json

                for k, v in with_txt.items():
                    for k1, v1 in no_txt.items():
                        if k == k1:  # если название папок совпадает, то склеиваем

                            # на верхнем уровне у json два ключа 'userForm' и 'completeTasks',
                            # первая часть одинакова, пересохраняем ее
                            new['userForm'] = v['userForm']

                            sub_json = []  # подсловари
                            for sub_json_1 in v['completeTasks']:

                                for i in sub_json_1['files']:
                                    if i['fileName'][:-3] == txt['file_name'][:-3]:
                                        sub_json_1['task']['text'] = txt['text']
                                        sub_json.append(sub_json_1)

                                for sub_json_2 in v1['completeTasks']:
                                    for j in sub_json_2['files']:
                                        if j['fileName'][:-3] == txt['file_name'][:-3]:
                                            sub_json_2['task']['text'] = txt['text']
                                            sub_json.append(sub_json_2)

                            new['completeTasks'] = sub_json  # новый склеиный json с дополненными текстовками

#
# if __name__ == '__main__':
#     Desktop = '/Users/Evelina/Desktop/'
#     PATH = 'nov'
#     fun(path=Desktop+PATH)

a = 5.465
print(round(a, 2))
