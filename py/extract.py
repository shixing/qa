import os
import json
from docx import Document
import xlrd
import json

d = {}

import sys

target = sys.argv[1]

data_dir = "../data/"+target

def convert(v):
    if type(v) == unicode:
        return v.encode('utf8')
    else:
        return str(v)

def para2text(p):
    rs = p._element.xpath('.//w:t')
    return u" ".join([r.text for r in rs])



for folder in os.listdir(data_dir):
    path = os.path.join(data_dir, folder)
    if os.path.isdir( path ):
        d[folder] = {"text":"","qas":[]}
        for fn in os.listdir(path):
            fp = os.path.join(path,fn)
            if fn.endswith('.docx') and not fn.startswith("~$"):
                doc = Document(fp)
                t = ""
                for p in doc.paragraphs:
                    t += convert(para2text(p)) + "\n"
                d[folder]["text"] = t
            if fn.endswith('.xlsx') and not fn.startswith("~$"):
                x = xlrd.open_workbook(fp)
                sheet = x.sheet_by_index(0)
                for irow in xrange(1, sheet.nrows):
                    q = sheet.row(irow)[1].value
                    a = sheet.row(irow)[2].value
                    q = convert(q)
                    a = convert(a)
                    d[folder]['qas'].append({"q":q,"a":a})

f = open('../{}.json'.format(target),'w')            
json.dump(d,f)
f.close()

