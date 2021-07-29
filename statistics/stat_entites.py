import json
import nltk
import csv
import pprint

FOLDER = '/Users/Evelina/Desktop/классификатор/'

# В одной табличке правильно извлеченные сущности,
CORRECT_ANNOTATOR = 'correct_entities_from_2020_04_27_00_00_01_to_2020_05_10_23_59_59.json'

# а в другой то, что не распозналось.
INN = 'contractors_incorrect_entities.json'


# чтение документа
def read_data(path):
    dataset = []
    for line in open(path, 'r').readlines():
        for key, value in json.loads(line).items():
            dataset.append(value)
    return dataset


###########################################################################################
def main_fun():

    # таблица с извленеченными сущностями, которые не распознались
    unrecognized = read_data(path=FOLDER + INN)

    result = {'не распознанные cущности': [],
              'не определена некорректная форма': [],
              'не определена корректная форма': [],
              'извлеклось с разницей в прописных/заглавных буквах': [],
              'полное не совпадение излеченных цифр': [],
              'не совпадает одна из излеченных цифр': [],
              'неверное распознание названия организации (ПАО)': [],
              'грамматическая ошибка в распознании названия организации (ПАО)': [],
              'прочее': []}

    full_check = 0
    for l in unrecognized:
        for data in l.values():

            full_check += 1
            correct = data['correct']
            incorrect = data['incorrect']

            for i in range(len(correct)):

                if correct[0] == incorrect[0] and correct[1] == incorrect[1]:
                    result['не распознанные cущности'].append(
                        {'correct': correct, 'incorrect': incorrect})

                elif correct == [None, None]:
                    result['не определена корректная форма'].append(
                        {'correct': correct, 'incorrect': incorrect})

                elif incorrect == [None, None]:
                    result['не определена некорректная форма'].append(
                        {'correct': correct, 'incorrect': incorrect})

                elif type(correct[0]) == int and type(correct[1]) == int \
                        and type(incorrect[0]) == int and type(incorrect[1]) == int:

                    if correct[0] != incorrect[0] and correct[1] != incorrect[1]:

                        result['полное не совпадение излеченных цифр'].append(
                            {'correct': correct, 'incorrect': incorrect})

                    elif correct[0] != incorrect[0] or correct[1] != incorrect[1]:
                        result['не совпадает одна из излеченных цифр'].append(
                            {'correct': correct, 'incorrect': incorrect})

                elif type(correct[0]) != int and type(correct[1]) != int \
                        and type(incorrect[0]) != int and type(incorrect[1]) != int:

                    correct[0] = correct[0].lower()
                    correct[1] = correct[1].lower()
                    incorrect[0] = incorrect[0].lower()
                    incorrect[1] = incorrect[1].lower()

                    if correct[0] == incorrect[0] and \
                            correct[1] == incorrect[1]:
                        result['извлеклось с разницей в прописных/заглавных буквах'].append(
                            {'correct': correct, 'incorrect': incorrect})

                    # добавить токенизацию и удаление пунктуации после сравнењия
                    # (добавочный пункт )

                    elif correct[0] == incorrect[0]:
                        if 'пао' in nltk.word_tokenize(correct[1]) or \
                                'пао' in nltk.word_tokenize(incorrect[1]):
                            result['неверное распознание названия организации (ПАО)'].append(
                                {'correct': correct, 'incorrect': incorrect})
                        else:
                            result['грамматическая ошибка в распознании названия организации (ПАО)'].append(
                                {'correct': correct, 'incorrect': incorrect})
                    elif correct[1] == incorrect[1]:
                        if 'пао' in nltk.word_tokenize(correct[0]) or \
                                'пао' in nltk.word_tokenize(incorrect[0]):
                            result['неверное распознание названия организации (ПАО)'].append(
                                {'correct': correct, 'incorrect': incorrect})
                        else:
                            result['грамматическая ошибка в распознании названия организации (ПАО)'].append(
                                {'correct': correct, 'incorrect': incorrect})

                    else:
                        result['прочее'].append(
                            {'correct': correct, 'incorrect': incorrect})

    # расчет и сохранение статистики по классам
    with open('/Users/Evelina/Desktop/' + 'stat_contractors_incorrect_entities.csv', "w", newline="") as file:
        columns = ["название", "процент опечаток данного класса относительно всех опечаток"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows([{"название": k,
                           "процент опечаток данного класса относительно всех опечаток":
                               round((len(v)/full_check)*100, 3)} for k, v in result.items()])

    # сохранение сущностей распределенных по классам
    with open('/Users/Evelina/Desktop/' + 'result.json', 'w') as output:
        output.write(json.dumps(result, ensure_ascii=False))

    for k, v in result.items():

        if k == 'прочее':

            value = [[value for value in i.values()] for i in v]

            for i in value:
                print(i)

            #     print (set(i[0]) ^ set(i[1]))
                # for kk, vv in i.items():
                #
                #     print(set([a for a in vv[0]]) ^ set([a for a in vv[1]]))


main_fun()