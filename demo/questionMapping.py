#!/usr/bin/python                                                                                                                                                                                                                
# coding=utf-8

# File Name: questionMapping.py
# Author   : john
# company  : foxconn
# Mail     : john.y.ke@mail.foxconn.com 
# Created Time: 2018/12/25 10:51
# Describe :

from refo import finditer, Predicate, Star, Any, Disjunction    # 正则表达式库
import re

# TODO SPARQL前缀和模板
SPARQL_PREXIX = u"""
    PREFIX : <http://www.poem.com#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX vocab: <http://localhost:2020/resource/vocab/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX map: <http://localhost:2020/resource/#>
    PREFIX db: <http://localhost:2020/resource/>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT DISTINCT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
             u"SELECT COUNT({select}) WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
             u"ASK {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


# TODO 定义关键词
pos_poet = "nr"   # 诗人名
pos_poem = "nz"  # 诗词名
pos_dynasty = "nt"    # 朝代
pos_verse = "x" # 诗句

poet_entity = (W(pos=pos_poet))
poem_entity = (W(pos=pos_poem))
dynasty_entity = (W(pos=pos_dynasty))
verse_entity = (W(pos=pos_verse))

poem = (W("诗") | W("词") | W("古诗") | W("诗词") | W("文章") | W("作品") | W("诗歌"))
poet = (W("诗人") | W("作者") | W("谁"))
dynasty = (W("朝代") | W("年代") | W("时候") | W("时间") | W("时代"))
content = (W("内容"))
born = (W("出自"))
next_verse = (W("下一句") | W("下句"))
prev_verse = (W("上一句") | W("上句"))

'''1. 某个诗人写了哪些诗
2.某首诗是谁写的
3.哪个诗人是哪个朝代的
4.哪首诗是哪个朝代的
5.哪个朝代有哪些诗
6.哪个朝代有哪些诗人
8.诗歌具体内容
9.诗句是哪个诗人写的
10.诗句出自哪首诗
11.上一句
12.下一句'''
class Question:
    def __init__(self):
        pass

    @staticmethod
    def has_poem_question(word_objects):  # 某个诗人写了哪些诗
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_poet:
                e = u"?s :poetName '{poet}'." \
                    u"?s :poetProduction  ?m." \
                    u"?m :poemName ?x".format(poet=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_poet_question(word_objects):    # 某首诗是谁写的
        select = u"?n"

        sparql = None
        for w in word_objects:
            if w.pos == pos_poem:
                e = u"?s :poemName '{poem}'." \
                    u"?a :poetProduction ?s." \
                    u"?a :poetName ?n".format(poem=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def born_poet_question(word_objects):  # 哪个诗人是哪个朝代的
        select = u"?n"

        sparql = None
        for w in word_objects:
            if w.pos == pos_poet:
                e = u"?s :poetName '{poet}'." \
                    u"?s :poetDynasty ?n.".format(poet=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def born_poem_question(word_objects):  # 诗歌是哪个朝代的
        select = u"?n"

        sparql = None
        for w in word_objects:
            if w.pos == pos_poem:
                e = u"?s :poemName '{poem}'." \
                    u"?m :poetProduction ?s." \
                    u"?m :poetDynasty ?n.".format(poem=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def born_poets_question(word_objects):  # 哪个朝代有哪些诗人
        select = u"?n"

        sparql = None
        for w in word_objects:
            if w.pos == pos_dynasty:
                e = u"?s :poetDynasty '{dynasty}'." \
                    u"?s :poetName ?n.".format(dynasty=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def born_poems_question(word_objects):  # 哪个朝代有哪些诗歌
        select = u"?n"

        sparql = None
        for w in word_objects:
            if w.pos == pos_dynasty:
                e = u"?s :poetDynasty '{dynasty}'." \
                    u"?s :poetProduction ?m." \
                    u"?m :poemName ?n.".format(dynasty=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def poets_content_question(word_objects):  # 诗歌内容
        select = u"?n"

        sparql = None
        for w in word_objects:
            if w.pos == pos_poem:
                e = u"?s :poemName '{poem}'." \
                    u"?s :poemContent ?n.".format(poem=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def poet_verse_question(word_objects):  # 按句找作者
        select = u"?o"

        sparql = None
        for w in word_objects:
            if w.pos == pos_verse:
                e = u"?s :verseContent '{verse}'." \
                    u"?s :verseIn ?m." \
                    u"?n :poetProduction ?m."\
                    u"?n :poetName ?o.".format(verse=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def poem_verse_question(word_objects):  # 按句查诗
        select = u"?o"

        sparql = None
        for w in word_objects:
            if w.pos == pos_verse:
                e = u"?s :verseContent '{verse}'." \
                    u"?s :verseIn ?m." \
                    u"?m :poemName ?o.".format(verse=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def next_verse_question(word_objects):  # 下一句
        select = u"?o"

        sparql = None
        for w in word_objects:
            if w.pos == pos_verse:
                e = u"?s :verseContent '{verse}'." \
                    u"?s :verseId ?m." \
                    u"?s :sentenceId ?n." \
                    u"?s :verseLen ?l." \
                    u"?k :verseId ?x." \
                    u"?k :sentenceId ?y." \
                    u"?k :verseContent ?o." \
                    u"filter ((?x = ?m) && (?y = ?n +1) && (?y <= ?l))".format(verse=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def prev_verse_question(word_objects):  # 上一句
        select = u"?o"

        sparql = None
        for w in word_objects:
            if w.pos == pos_verse:
                e = u"?s :verseContent'{verse}'." \
                    u"?s :verseId ?m." \
                    u"?s :sentenceId ?n." \
                    u"?k :verseId ?x." \
                    u"?k :sentenceId ?y." \
                    u"?k :verseContent ?o." \
                    u"FILTER ((?x = ?m) && (?y = ?n - 1) && (?n > 1))".format(verse=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

rules = [
    Rule(condition_num=2, condition=((poet_entity + Star(Any(), greedy=False) + poem + Star(Any(), greedy=False)) | (poem + Star(Any(), greedy=False) + poet_entity + Star(Any(), greedy=False))), action=Question.has_poem_question),
    Rule(condition_num=2, condition=((poem_entity + Star(Any(), greedy=False) + poet + Star(Any(), greedy=False)) | (poet + Star(Any(), greedy=False) + poem_entity + Star(Any(), greedy=False))), action=Question.has_poet_question),
    Rule(condition_num=2, condition=(poet_entity + Star(Any(), greedy=False) + dynasty + Star(Any(), greedy=False)), action=Question.born_poet_question),
    Rule(condition_num=2, condition=(poem_entity + Star(Any(), greedy=False) + dynasty + Star(Any(), greedy=False)), action=Question.born_poem_question),
    Rule(condition_num=2, condition=((dynasty_entity + Star(Any(), greedy=False) + poem + Star(Any(), greedy=False)) | (poem + Star(Any(), greedy=False) + dynasty_entity + Star(Any(), greedy=False))), action=Question.born_poems_question),
    Rule(condition_num=2, condition=((dynasty_entity + Star(Any(), greedy=False) + poet + Star(Any(), greedy=False)) | (poet + Star(Any(), greedy=False) + dynasty_entity + Star(Any(), greedy=False))), action=Question.born_poets_question),
    Rule(condition_num=1, condition=(poem_entity + Star(Any(), greedy=False)), action=Question.poets_content_question),
    Rule(condition_num=2, condition=((verse_entity + Star(Any(), greedy=False) + poet + Star(Any(), greedy=False)) | (poet + Star(Any(), greedy=False) + verse_entity + Star(Any(), greedy=False))), action=Question.poet_verse_question),
    Rule(condition_num=2, condition=((verse_entity + Star(Any(), greedy=False) + poem + Star(Any(), greedy=False)) | (poem + Star(Any(), greedy=False) + verse_entity + Star(Any(), greedy=False))), action=Question.poem_verse_question),
    Rule(condition_num=2, condition=(verse_entity + Star(Any(), greedy=False) + next_verse + Star(Any(), greedy=False)), action=Question.next_verse_question),
    Rule(condition_num=2, condition=(verse_entity + Star(Any(), greedy=False) + prev_verse + Star(Any(), greedy=False)), action=Question.prev_verse_question)
]
