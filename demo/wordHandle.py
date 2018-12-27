#!/usr/bin/python                                                                                                                                                                                                                
# coding=utf-8

# File Name: wordHandle.py
# Author   : john
# company  : foxconn
# Mail     : john.y.ke@mail.foxconn.com 
# Created Time: 2018/12/25 10:50
# Describe :

import jieba
import jieba.posseg as psg

class Word:
    def __init__(self, token, pos):
        self.token = token  # 分词
        self.pos = pos  # 词性

class Tagger:
    def __init__(self, dict_paths):
        for p in dict_paths:
            jieba.load_userdict(p)  # 加载外部词典

    def get_word_objects(self, sentence):
        #print([word for word in psg.cut(sentence)])
        return [Word(word, tag) for word, tag in psg.cut(sentence)]  #分词，获取单词与词性