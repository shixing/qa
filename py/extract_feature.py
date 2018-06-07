import os
import sys
import json
import jieba
from ppdb import extract_ppdb

target = sys.argv[1]

json_file = "../{}.json".format(target)

f = open(json_file)
d = json.load(f) # d = {"folder":{"text":}}
f.close()

# split sentence with circle and \n

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

def print_sents(sents):
    for words in sents:
        print " ".join([u"[{}]".format(x) for x in words])
    print '----'

def subof(a,b):
    # a is sub of b
    for i in xrange(len(b) - len(a) + 1):
        for j in xrange(len(a)):
            if a[j] != b[i+j]:
                break
            if j == len(a) - 1:
                return True
    return False

def which_sent(query, sents):
    for i in xrange(len(sents)):
        if subof(query, sents[i]):
            return i
    return -1


def get_coverage(query, candidates, ppdb):

    do_ppdb = False

    
    n = len(query)
    d = {}
    for candidate in candidates:
        for t in candidate:
            d[t] = 1

    c = 0
    for t in query:
        if t in d:
            c+=1
        elif do_ppdb:
            if t in ppdb:
                if ppdb[t][0] in d:
                    print t, ppdb[t][0], ppdb[t][1]
                    print ppdb[t][0] in d
                    c+=1

    return c * 1.0 / n 


def top_n(query, candidates, n, ppdb):
    scores = []
    pre_n , post_n = 3, 0
    for i, candidate in enumerate(candidates):
        if i < pre_n:
            start = 0
        else:
            start = i - pre_n
        if i > len(candidates) - 1 - post_n:
            end = len(candidate) - 1
        else:
            end = i + 1 + post_n
            
        span = candidates[start:end]
        
        score = get_coverage(query, span, ppdb)
        scores.append((i, score))

    scores = sorted(scores, key = lambda x: -x[1])

    return scores[:n]



# extract features

# positive/negative ratio: 1/3
## negative example, most similar positive 

# For multiple sents answer, just 

pdb = None #extract_ppdb("../data/ppdb-1.0-s-lexical")


n_total, hit_total = 0,0

for folder in d:
    folder_t = tokenize_split_sentence(folder)
    
    text = d[folder]['text']
    
    text_t = tokenize_split_sentence(text)

    #print_sents(text_t)
    
    qas = d[folder]['qas']

    n , hit = 0,0
    
    for qai, qa in enumerate(qas):
        q = qa['q']
        a = qa['a']

        q_t = tokenize_split_sentence(q)
        a_t = tokenize_split_sentence(a)

        
        sent_id = which_sent(a_t[0], text_t)

        
        if sent_id != -1:
            n += 1
            #print qai
            #print_sents(q_t)
            #print_sents(a_t)
            #print "BUILD FEATURE"

            negs = top_n(q_t[0], text_t,  4, pdb)

            if negs[0][0] == sent_id:
                hit += 1
            else:
                print "Question:", 
                print_sents(q_t)
                print "Answer:",
                print_sents(a_t)
                print "Candidates:"
                for tid, score in negs:
                    print score,
                    print_sents([text_t[tid]])
                print "================="
            
            #build_feature(text_t, sent_id, q_t, a_t)
            
        else:
            pass
            #print "NOT IN TEXT"

    print n, hit
    n_total += n
    hit_total += hit
    break
    
print n_total, hit_total
            
    


