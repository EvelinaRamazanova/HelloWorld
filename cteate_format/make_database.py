import os
import json
import pandas as pd
import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
import typing as t

PATH = '/home/evelina/Рабочий стол/iteration/'
FOLDER = '30/'
PATH_TO_CSV = '/home/evelina/Рабочий стол/comments.csv'


def draw_images(
        block_type: str,
        filename: str,
        images_list: list,
        orient: str = 'horizontal',
        figsize: tuple = (10, 15)):
    """
    Images drawing function

    :param block_type: type class attributes
    :param filename: images name
    :param images_list: images list
    :param orient: images orientation
    :param figsize: images size
    :return:
    """
    check_images = len(images_list)
    fig = plt.figure(figsize=figsize)
    for i, image in enumerate(images_list):
        if orient == 'horizontal':
            ax = fig.add_subplot(1, check_images, i + 1)
        elif orient == 'vertical':
            ax = fig.add_subplot(check_images, 1, i + 1)
        else:
            raise ValueError
        ax.imshow(image)
    plt.title('Имя файла: {}\nКласс: {}'.format(filename, block_type))
    plt.show()


def comment(path: t.Text):
    """
    Function to read csv-file with a set of exception images
    :param path: path to csv-file
    :return:
    """
    comment_list = set()
    for row in csv.reader(open(path, 'r'), delimiter=';', quotechar='"'):
        comment_list.add(row[2])
    return comment_list


def path_doc(path: t.Text):
    """
    List of paths to data
    :param path: path to data
    :return:
    """
    filePath = []
    for top, dirs, files in os.walk(path):
        for fileName in files:
            filePath.append(os.path.join(top, fileName))
    return filePath


def _get_json(file: t.Text):
    """
    Read a file as a set of json lines
    :param file: file for read
    :return:
    """
    with open(file, 'r') as f:
        distros_dict = json.load(f)
    return distros_dict


def tab_colum(span: t.Dict):
    """
    Attribute counting function
    :param span: dictionary containing key values that are necessary attributes
    :return:
    """
    x = span['shape_attributes']['x']
    y = span['shape_attributes']['y']
    w = span['shape_attributes']['width']
    h = span['shape_attributes']['height']
    attributes = (x, y, w, h)
    return attributes


def make_full_dataset(
        path: t.Text,
        path_to_csv: t.Text,
        folder: t.Text):
    """
    Read and draw images, collection and save statistics on them

    :param path:
    :param path_to_csv:
    :param folder:
    :return:
    """
    # filedir = path_doc(path)

    filedir = os.path.join(path + folder)
    os.chdir(filedir)

    attributes_list = []
    for file in os.listdir(filedir):
        if file == 'via_project_complete.json':
            json_file = _get_json(file)
            for value in json_file['_via_img_metadata'].values():

                if value['filename'] in comment(path_to_csv):
                    continue

                filename = value['filename']
                name = {'filename': filename}

                image = cv2.imread(path + folder + filename)
                if image is None:
                    print(file)
                    continue

                keys_list = ['text', 'sign', 'header', 'number', 'preamble', 'requisites', 'stamp', 'table']

                labels = {k: [] for k in keys_list}
                for span in value['regions']:
                    block_type = span['region_attributes']['type']
                    if block_type in keys_list:

                        span_mask = np.zeros(shape=image.shape[:2], dtype=np.uint8)

                        x = span['shape_attributes']['x']
                        y = span['shape_attributes']['y']
                        w = span['shape_attributes']['width']
                        h = span['shape_attributes']['height']

                        span_mask[y: y + h, x: x + w] = 1
                        draw_images(block_type, filename, [image, span_mask])

                        labels[block_type].append(tab_colum(span))

                name.update(labels)
                name = {k: -1 if not v else v for k, v in name.items()}
                attributes_list.append(name)

    df = pd.DataFrame(data=attributes_list)
    print(df)
    df.to_csv(path + 'test.csv', sep=';', index=False)


make_full_dataset(PATH, PATH_TO_CSV, FOLDER)
