# -*- coding: utf8 -*-
import csv
import sys
import nltk
import json
import string

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer

csv.field_size_limit(sys.maxsize)


#####################################################################
# чтение датасета
# объединение всех блоков с текстом в цельный документ
def read_data(path):

    docs = []
    for line in csv.reader(open(path, 'r'), delimiter='\t'):
        if line[1] == '':
            continue
        lst = []
        try:
            for blocks in json.loads(line[1]).values():
                for text in blocks['blocks'].values():
                    lst.append(text['text'])
        except KeyError:
            continue
        docs.append('\n'.join(lst))
    print('Сформирован датасет')
    return docs
#####################################################################


# чтение строки файла словаря
def dictionary_words(path):
    file = open(path, 'r').read().split('\n')
    dictionary = set([line.lower() for line in file])
    ln = len(dictionary)
    print('Сформировал словарь (Длина словаря: {})'.format(ln))
    return dictionary


# предобработка
def filter_doc(dict_words, mts_docs):

    dict_list = dictionary_words(dict_words)
    data_list = read_data(mts_docs)

    docs = []
    for doc in data_list:

        # разбиваем на токены
        lst = []
        tokens = nltk.wordpunct_tokenize(doc)

        # удаляем пунктуацию и цифры
        for token in tokens:
            if token not in string.digits and \
                 token not in string.punctuation:
                lst.append(token)

        # смотрим процент чистоты текста (более 50)
        i = 0
        for token in lst:
            if token in dict_list:
                i += 1
        stat = (i*100)/len(lst)

        if stat > 50:
            docs.append(' '.join(lst))
    return docs


def tf_idf():

    corpus = filter_doc(dict_words=FOLDER+DICT_WORDS,
                        mts_docs=FOLDER+MTS_DOC)
    tfidf = TfidfVectorizer(
        min_df=5,
        max_df=0.95,
        max_features=8000,
        stop_words='english'
    )
    tfidf.fit(corpus)
    text = tfidf.transform(corpus)

    def find_optimal_clusters(data, max_k):
        iters = range(2, max_k + 1, 2)

        sse = []
        for k in iters:
            sse.append(MiniBatchKMeans(n_clusters=k, init_size=1024, batch_size=2048, random_state=20).fit(data).inertia_)
            print('Fit {} clusters'.format(k))

        f, ax = plt.subplots(1, 1)
        ax.plot(iters, sse, marker='o')
        ax.set_xlabel('Cluster Centers')
        ax.set_xticks(iters)
        ax.set_xticklabels(iters)
        ax.set_ylabel('SSE')
        ax.set_title('SSE by Cluster Center Plot')

        # plt.show()

    n_clusters = 150  # кол-во классов
    find_optimal_clusters(text, n_clusters)
    clusters = MiniBatchKMeans(n_clusters=n_clusters, init_size=1024, batch_size=2048, random_state=20).fit_predict(text)

    def get_top_keywords(data, clusters, labels, n_terms):
        df = pd.DataFrame(data.todense()).groupby(clusters).mean()

        for i, r in df.iterrows():
            print('\nCluster {}'.format(i))
            print(','.join([labels[t] for t in np.argsort(r)[-n_terms:]]))

    get_top_keywords(text, clusters, tfidf.get_feature_names(), 10)


FOLDER = '/Users/Evelina/Desktop/'
MTS_DOC = 'content_27.04.2020.tsv'
DICT_WORDS = 'doccano/dict_full.txt'

tf_idf()