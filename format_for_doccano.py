import os
import json

PATH = '/home/evelina/Рабочий стол/1/'
PATH_OUT = '/home/evelina/Рабочий стол/sort_medsi_makeup/annotated/'


def la(path, path2):

    with open(path2 + '1-40.json', 'w'):
        pass

    filedir = os.path.join(path)
    os.chdir(filedir)

    lst = os.listdir(filedir)
    bla = (lst[328:368])  # первые 3 дока
    i = 0
    for file in bla:
        print(file)
        if file.endswith('.json'):
            f = open(file, 'r')
            reader = f.read()
            print(reader)

            i = i+1
            with open(path2 + '328-368.json', 'a', newline='') as w:
                w.write(reader)
    print(i)


la(PATH_OUT, PATH)