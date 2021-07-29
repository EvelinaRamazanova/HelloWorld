import csv
import sys
import json
import nltk
import re

csv.field_size_limit(sys.maxsize)
FOLDER = '/Users/Evelina/Desktop/'
CONTENT = 'content_27.04.2020.json'


# чтение датасета
def read_dataset(path):
    return [json.loads(doc) for doc in open(path, 'r')]


def main():

    i = 0

    keys_list = ['% от стоимости монтажа',
                 'наценка',
                 '% от ежемесячной стоимости услуг',
                 'неустойки',
                 '% от стоимости перевозки',
                 '% от переданных прав требований',
                 '% от стоимости смр',
                 '% от стоимости пунктов',
                 '% от стоимости демонтажа',
                 '% от стоимости работ',
                 '% от цены договора',
                 '% от стоимости заказа']

    dict_block = {k: [] for k in keys_list}

    data = read_dataset(FOLDER+CONTENT)
    for doc in data:
        list_block = doc['text']

        if len(list_block) == 0:
            continue

        for j in range(0, len(list_block)-1):

            if len(list_block[j]) < 5:
                continue

            elif '% от' not in list_block[j]:
                continue

            elif 'НДС' in list_block[j] or \
                    ' от протяженности трассы' in list_block[j].lower():
                continue

            elif re.findall('% от высоты', ''.join(list_block[j:j + 3]).lower()):
                continue

            ###########################################################################

            elif re.findall('от монтажа|от стоимости монтажа|от \\nстоимости монтажа|от\\nстоимости монтажа|стоимости \nмонтажа', list_block[j].lower()):
                dict_block['% от стоимости монтажа'].append(list_block[j])
            elif '% от стоимости' in list_block[j].lower() and 'монтажа' in list_block[j:j+4]:
                dict_block['% от стоимости монтажа'].append(list_block[j])
            elif 'демонтаж' in list_block[j].lower() and 'монтажа' in list_block[j] or \
                    re.findall('% от дм|дм|демонтаж', ''.join(list_block[j:j+3]).lower()):
                dict_block['% от стоимости демонтажа'].append(list_block[j])

            elif re.findall('% от ежемесячной стоимости услуг', list_block[j].lower()):
                dict_block['% от ежемесячной стоимости услуг'].append(list_block[j])

            elif re.findall('неустойки', list_block[j].lower()):
                dict_block['неустойки'].append(list_block[j])

            elif re.findall('% от стоимости перевозки', list_block[j].lower()):
                dict_block['% от стоимости перевозки'].append(list_block[j])

            elif re.findall('% от переданных прав требований', list_block[j].lower()):
                dict_block['% от переданных прав требований'].append(list_block[j])

            elif re.findall('% от стоимости смр|% от смр', ''.join(list_block[j:j+3]).lower()):
                dict_block['% от стоимости смр'].append(list_block[j])

            elif re.findall('% от стоимости пунктов', ''.join(list_block[j:j+3]).lower()):
                dict_block['% от стоимости пунктов'].append(list_block[j])

            elif re.findall('% от стоимости работ', ''.join(list_block[j:j+3]).lower()):
                dict_block['% от стоимости работ'].append(list_block[j])

            elif re.findall('% от цены договора', ''.join(list_block[j:j+3]).lower()):
                dict_block['% от цены договора'].append(list_block[j])

            elif re.findall('% от стоимости заказа', ''.join(list_block[j:j+3]).lower()):
                dict_block['% от стоимости заказа'].append(list_block[j])

            else:
                print(list_block[j:j+4])
                print('#'*30)

                i += 1

    print('i', i)

    for k, v in dict_block.items():
        print('{}: {} шт.'.format(k, len(v)))



main()