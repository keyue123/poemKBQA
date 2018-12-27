#!/usr/bin/python                                                                                                                                                                                                                
# coding=utf-8

# File Name: fileHandle.py
# Author   : john
# company  : foxconn
# Mail     : john.y.ke@mail.foxconn.com 
# Created Time: 2018/12/24 18:15
# Describe :

import csv
import pandas as pd

#诗人id与作品id对应
'''poet_df = pd.read_csv(u'C:\\Users\\John\\Desktop\\诗词\\poet.csv', engine='python')
poem_df = pd.read_csv(u'C:\\Users\\John\\Desktop\\诗词\\poet_to_poem.csv', engine='python')

for i in range(len(poem_df)):
    for line in poet_df.values:
        if poem_df.loc[i, 'poet_id'] == line[1]:
            poem_df.loc[i, 'poet_id'] = line[0]

poem_df.to_csv(u'C:\\Users\\John\\Desktop\\诗词\\poet_t_poem.csv', header=['poem_id', 'poet_id', 'content'])'''


f_poem = open(u'C:\\Users\\John\\Desktop\\诗词\\sentence.csv', 'r', encoding='utf-8')
f_sentence = open(u'C:\\Users\\John\\Desktop\\诗词\\poem_sentence.csv', 'a', encoding='utf-8')
reader = csv.reader(f_poem)
writer = csv.writer(f_sentence)
for row in reader:

    poem_id = row[0]
    count = 0
    sentences = row[2].split('，')
    num = len(sentences)
    for i in range(num):
        poem_sentence = []
        count = count + 1
        poem_sentence.append(poem_id)
        poem_sentence.append(count)
        poem_sentence.append(num)
        poem_sentence.append(sentences[i])
        print(poem_sentence)
        writer.writerow(poem_sentence)