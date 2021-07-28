from PyPDF2 import PdfFileWriter, PdfFileReader
import os

PATH = '/home/evelina/Рабочий стол/акты для скрытия/акты для скрытия/'
FOLDER_1 = 'Подписанные ЗП 2019'
FOLDER_2 = 'Подписанные ЗП 2019 - 2'
FOLDER_3 = 'Рамки'

path = PATH + FOLDER_1 + '/'

for file in os.listdir(path):
    print(file)


def solution(path, file):
    with open(path + file, "rb") as in_f:
        input1 = PdfFileReader(in_f)
        output = PdfFileWriter()

        numPages = input1.getNumPages()
        print("document has %s pages." % numPages)

        for i in range(numPages):
            page = input1.getPage(i)
            print('Стр. № {} -- Ширина: {}, Высота: {}'.format
                  (i, page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y()))

            if i in [1, 3, 4, 5, 6, 7]:
                output.addPage(page)
                continue

            if i == 0:
                y = 290  # right point
                page.mediaBox.lowerRight = (y, 0)
                page.mediaBox.lowerLeft = (0, 0)
                page.mediaBox.upperRight = (y, 841)
                page.mediaBox.upperLeft = (0, 841)
                output.addPage(page)
                continue

            """if i == 0:
                x = 595  # right point
                y = 440
                page.mediaBox.lowerRight = (x, 0)
                page.mediaBox.lowerLeft = (0, 0)
                page.mediaBox.upperRight = (x, y)
                page.mediaBox.upperLeft = (0, y)
                output.addPage(page)
                continue"""

            if i == 2:
                x = 310
                y = 850  # right point
                page.mediaBox.lowerRight = (x, 0)
                page.mediaBox.lowerLeft = (0, 0)
                page.mediaBox.upperRight = (x, y)
                page.mediaBox.upperLeft = (0, y)

                output.addPage(page)

        with open(path + "new_%s" % file, "wb") as out_f:
            output.write(out_f)


solution(path=path, file='2019-11.pdf')