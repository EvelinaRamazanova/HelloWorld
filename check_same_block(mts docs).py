import csv
import sys
import json
from collections import Counter
import pprint

csv.field_size_limit(sys.maxsize)
FOLDER = '/Users/Evelina/Desktop/'
CONTENT = 'content_27.04.2020.json'


# чтение датасета
def read_dataset(path):
    return [json.loads(doc)['text'] for doc in open(path, 'r')]


def check_blocks():

    array = []
    for doc in read_dataset(FOLDER + CONTENT):
        for list_block in doc:
            if len(list_block) > 20:

                array.append(list_block)

    return Counter(array)


def main():

    result = {}
    for k, v in check_blocks().items():
        if v > 30:
            result[k] = v

        # print('текст блока: ', k[0:30], '; повторений: ', v)

    pprint.pprint(result)

    with open(FOLDER+'result.json', 'w') as file:
        file.write(json.dumps(result, ensure_ascii=False))


main()