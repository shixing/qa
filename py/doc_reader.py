import os
import json
from docx import Document
import xlrd
import json
import sys
import jieba
from ppdb import extract_ppdb


def convert(v):
    if type(v) == unicode:
        return v.encode('utf8')
    else:
        return str(v)

def para2text(p):
    rs = p._element.xpath('.//w:t')
    return u" ".join([r.text for r in rs])

def docx2text(fn):
    doc = Document(fn)
    t = ""
    for p in doc.paragraphs:
        t +=  para2text(p) + "\n"
    #print(t)
    return t

################################

def remove_space(tokens):
    ll = []
    for t in tokens:
        if t == ' ' or t == '' or t == '\t':
            continue
        ll.append(t)
    return ll


def tokenize_split_sentence(lines):
    # p should be unicode
    sents = []
    for p in lines.split('\n'):
        tokens = remove_space(jieba.cut(p))
        sent = []
        for t in tokens:
            if t == u'\u3002':
                sent.append(t)
                sents.append(sent)
                sent = []
            else:
                sent.append(t)
        if len(sent) > 0:
            sents.append(sent)
    return sents
