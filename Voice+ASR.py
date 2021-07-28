import os
import shutil
import json
import re


def new_folder(path):
    """
    Создадим папки куда будем складывать отсортированные данные
    """
    os.mkdir(path + 'result/данные без отекстовок')
    os.mkdir(path + 'result/данные с отекстовками')
    os.mkdir(path + 'result/json/json без отекстовок')
    os.mkdir(path + 'result/json/json с отекстовками')


def del_empty_dirs(path, folder_without_re_txt):
    """
    Удаление пустых папок.
    Если в папке отсутствуют json-файлы вообще, помещаем ее в папку "данные без отекстовок".

    param:
    path - путь до папки с данными, которые нужно отсортировать
    new_folders - папка, куда складываются файлы, которые не содержат json
    """

    for folders, sub_dirs, files in os.walk(path, topdown=False):
        if len(os.listdir(folders)) == 0:
            os.rmdir(folders)  # удаление пустых папок
        elif 'json.json' not in files:
            new_folders = folder_without_re_txt+folders.split('/')[-1]

            if folders != path:  # исклчаем ключевую папку sep4, sep5, dec и тд
                shutil.move(folders, new_folders)  # перенос папок, без json файла


def filter_audio(path, directory):
    """
        Слова "Начитай фразу" в текстовку не включаем.
        Аудиофайлы по заданиям "Расскажи рассказ по картинке" необходимо поместить в
        отдельную папку или архив с названием "Без текстовок".
        Вытащить из json файла текст для каждого аудио и сохранить в одноименных
        с аудиофайлами текстовиках.
        Файлы (картинки, начитки), к которым нет начитки, переносим.
        Распарсить json, расбить json на два : с оттекстовкой и без нее

        param:
        path -  путь до папки с данными, которые нужно отсортировать
        directory - путь до папки, куда складываются данные без отекстовок
        """

    json_with_text = {}  # словарь с начиткой
    json_without_text = {}  # словарь без начитки

    for folders, sub_dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name == 'json.json':
                json_file = json.load(open(os.path.join(folders, name), 'r'))  # json одной папки

                # на верхнем уровне у json два ключа 'userForm' и 'completeTasks',
                # первая часть одинакова, пересохраняем ее
                json_with_text['userForm'] = json_file['userForm']
                json_without_text['userForm'] = json_file['userForm']

                sub_json_txt = []  # подсловари с начиткой
                sub_json_no_txt = []  # подсловари без начитки
                for sub_json in json_file['completeTasks']:

                    description = {}  # удаление скобок из формата словаря [{-словарь-}]
                    text = sub_json['task']['text']
                    for line in sub_json['files']:
                        for k, v in line.items():
                            description[k] = v

                    second_name = description['fileName'][0:-4] + ".txt"  # меняем расширение в имени

                    d = {}
                    if "Начитай в микрофон фразу" in text:
                        text = (re.sub(r"Начитай в микрофон фразу: ", "", text))
                        d[second_name] = text
                        sub_json_txt.append(sub_json)

                    elif "Расскажи рассказ по картинке" in text or \
                            "Опишите историю из сюжетов на картинке" in text:
                        sub_json_no_txt.append(sub_json)

                    else:
                        d[second_name] = text  # сохраняем словарь {имя: текст аудио} для дальнейшего сохранения в .txt
                        sub_json_txt.append(sub_json)  # сохранение вложенения от 'completeTasks'

                    if "Расскажи рассказ по картинке" in text or \
                            "Опишите историю из сюжетов на картинке" in text:
                        # новая директория для аудиофайлов начинающихся на "Расскажи рассказ по картинке"

                        try:
                            if not os.path.exists(directory + folders.split('/')[-1]):
                                os.makedirs(directory + folders.split('/')[-1])
                            shutil.move(folders + '/' + description['fileName'],
                                        directory+folders.split('/')[-1] + '/' + description['fileName'])
                        except FileNotFoundError:
                            pass

                    # сохранение текстовок
                    for s_name, txt in d.items():
                        with open(folders+'/'+s_name, 'w') as wrt:
                            wrt.write(txt)

                # сохранение всех вложений и формирование уже разделенных на 'с текстовками' и 'без текстовок' словарей
                json_with_text['completeTasks'] = sub_json_txt
                json_without_text['completeTasks'] = sub_json_no_txt

    # создадимм папки для json и сохраним их туда
    for folder_name in os.listdir(path):

        if not os.path.exists(JSON_NO_TXT + folder_name):  # без оттекстовок
            os.makedirs(JSON_NO_TXT + folder_name)

        if not os.path.exists(JSON_TXT + folder_name):  # с оттекстовками
            os.makedirs(JSON_TXT + folder_name)

        with open(JSON_NO_TXT + folder_name + '/' + 'no_text.json', 'w') as no_re_text, \
                open(JSON_TXT + folder_name + '/' + 'with_text.json', 'w') as re_tex:

            json.dump(json_with_text, re_tex, ensure_ascii=False, indent=4)
            json.dump(json_without_text, no_re_text, ensure_ascii=False, indent=4)

    # сохранение данных в папке 'c оттекстовками'
    for folder_name in os.listdir(path):
        if folder_name == '.DS_Store':
            pass
        else:
            for file in os.listdir(path + '/'+folder_name):
                if file != "json.json":
                    try:
                        if not os.path.exists(WITH_RE_TEXT+folder_name):
                            os.makedirs(WITH_RE_TEXT+folder_name)

                        shutil.move(path + "/" + folder_name + "/" + file,
                                    WITH_RE_TEXT + folder_name + "/" + file)
                    except FileNotFoundError:
                        pass


if __name__ == '__main__':

    # Файлы для работы все, кроме sep1.tar.gz, sep2.tar.gz и sep3.tar.gz
    Desktop = '/Users/Evelina/Desktop/'
    PATH = Desktop + 'nov'

    WITHOUT_RE_TEXT = Desktop + 'result/данные без отекстовок/'
    WITH_RE_TEXT = Desktop + 'result/данные с отекстовками/'
    JSON_TXT = Desktop + 'result/json/json_with_txt/'
    JSON_NO_TXT = Desktop + 'result/json/json_without_txt/'

    # new_folder(Desktop)  # создание папок
    del_empty_dirs(PATH, WITHOUT_RE_TEXT)  # удаление пустых папок.
    filter_audio(PATH, WITHOUT_RE_TEXT)  # основная функция фильтрующая исходные данные
