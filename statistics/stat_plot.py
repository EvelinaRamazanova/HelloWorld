import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

PATH = '/Users/Evelina/Desktop/'

# открываем таблицу со статистикой по документам
df = pd.read_csv(PATH + 'mistakes_ver_from_doc.csv',
                 names=['document', 'ver_typos'])

# оклугляем значение процента опечаток по док-ам
df['Процент опечаток документе'] = df['ver_typos'].apply(np.floor)

# группируем и подсчитываем кол-во док-ов с одинаковым процентом
df = df.groupby(['Процент опечаток документе']).size().reset_index(name='Кол-во док-ов с одинаковым процентом опечаток')

df = df.sort_values(by='Процент опечаток документе', ascending=True)
print(df)

df.plot(x='Процент опечаток документе', y='Кол-во док-ов с одинаковым процентом опечаток', figsize=(8, 6), kind='bar', rot=90)

plt.savefig('stat.png')
