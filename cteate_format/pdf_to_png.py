from pdf2image import convert_from_path
from PIL import Image
import os
import shutil
import glob

# папка с  pdf документами
PDF_DIR = r'/home/evelina/Документы/programms/pdf2im/pdf_dir'

# папка с получившимися изображениями
SAVED_DIR = '/home/evelina/Документы/programms/pdf2im/saved_dir/'


# поиск pdf в папке и перевод документа в список изображений
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


del_file_in_dir(SAVED_DIR)
pdf2image(PDF_DIR, SAVED_DIR)
