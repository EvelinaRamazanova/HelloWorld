# -*- coding: utf8 -*-

from pdf2image import convert_from_path
from PIL import Image

import os
import shutil
import glob

import pytesseract


REQUISITES = '/home/evelina/Документы/programms/pdf2im/requisites/'
HEADER = '/home/evelina/Документы/programms/pdf2im/header/'

PDF_DIR = r'/home/evelina/Документы/programms/pdf2im/pdf_dir/'

SAVED_DIR = '/home/evelina/Документы/programms/pdf2im/saved_dir/'


def pdf2image(path1, path2):
    pdf_dir = path1

    os.chdir(pdf_dir)

    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            pages = convert_from_path(pdf_file, dpi=300)

            pdf_file = pdf_file[:-4]

            for page in pages:
                page.save(path2+"%s(стр. %d).png" % (pdf_file, pages.index(page)), "PNG")
    print('~~ Файлы .pdf переведены в .png и сохранены ~~')


# удалениие файлов в папке
def del_file_in_dir(path):
    os.chdir(path)
    files = glob.glob('*.png')
    for filename in files:
        os.unlink(filename)
    print('~~ Директория очищена ~~')


# считывание текста с картинки
def tess(file):
    line_list = set()
    text_list = pytesseract.image_to_string(Image.open(file), lang='rus')
    text_low = text_list.lower()
    line = text_low.split('\n')
    for i in line:
        line_list.add(i)
    return line_list


def sort_jpg(path1, path2):
    os.chdir(path1)

    req = '№ фф/]р/150922/04'
    for jpg_file in os.listdir(path1):
        line_jpg = tess(jpg_file)
        # print(jpg_file)
        print(line_jpg)
        for line in line_jpg:
            if req in line:
                print("true", jpg_file)
                shutil.move(path1 + jpg_file, path2 + jpg_file)
                break


del_file_in_dir(SAVED_DIR)
# del_file_in_dir(REQUISITES)
pdf2image(PDF_DIR, SAVED_DIR)
# sort_jpg(SAVED_DIR, REQUISITES)
