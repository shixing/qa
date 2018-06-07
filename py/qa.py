from elasticsearch import Elasticsearch
from doc_reader import docx2text, tokenize_split_sentence
import os
from ppdb import extract_ppdb
from model import get_coverage, top_n

class QA:
    def __init__(self, doc_dir):
        self.doc_dir = doc_dir
        self.es = Elasticsearch()
        self.es.indices.delete(index='qa', ignore=[400, 404])

        self.ppdb = extract_ppdb('../data/ppdb-1.0-s-lexical')
        self.title2doc_id = {}
        self.build_search_index()

    def build_search_index(self):

        doc_id = 0
        for fn in os.listdir(self.doc_dir):
            fp = os.path.join(self.doc_dir,fn)
            if fn.endswith('.docx') and not fn.startswith("~$"):
                title = fn
                body = docx2text(fp)
                body_t = tokenize_split_sentence(body)
                doc = {}
                doc['title'] = title
                doc['text'] = body
                doc['body_t'] = body_t

                self.es.index(index="qa", doc_type="docx", id = doc_id, body = doc)
                self.title2doc_id[title] = doc_id
                
                doc_id += 1
        
        print("Index built")

    def predict(self, query, top_n_docs, k):
        res = self.es.search(index = "qa", doc_type="docx", body = {"query": {"match": {"title":query}}})
        answers = []
        for hit in res['hits']["hits"][:top_n_docs]:
            source = hit['_source']
            title, results = self.get_answer(source, query, k)
            answers.append((title, results))
        
        return answers


    def predict_single_doc(self, query, file_name, k):
        if file_name in self.title2doc_id:
            doc_id = self.title2doc_id[file_name]
            res = self.es.get(index="qa", doc_type='docx', id=doc_id)
            source = res['_source']
            title, results = self.get_answer(source, query, k)
            return [(title, results)]
        else:
            return None, []

        
    def get_answer(self, source, query, k):
        results = []
        title = None
        text_t = source['body_t']
        title = source['title']
        query_t = tokenize_split_sentence(query)
        index_scores = top_n(query_t[0], text_t, k, self.ppdb)

        for i, score in index_scores:
            sent = u"".join(text_t[i])
            results.append((sent, score))
        
        return title, results



    
