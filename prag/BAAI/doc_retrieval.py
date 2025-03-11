import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from FlagEmbedding import FlagReranker
from prag.docs.doc_loader import DocLoader

# default reranker model is 'BAAI/bge-reranker-v2-m3'
class DocRetrieval:
    '''
    DocRetrieval class for retrieving documents
    args:
        reranker: FlagReranker object

    methods:
        retrieve(query, passages): retrieve documents based on query and passages, return a sorted list of tuples (passage, score) \
            sorted by score in descending order.
    
    '''
    def __init__(self, reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)):
        self.reranker = reranker

    def retrieve(self, query, passages):
        # if passages is a list of strings
        if isinstance(passages, list) and isinstance(passages[0], str):
            scores = self.reranker.compute_score([[query, p] for p in passages], normalize=True)
            # return sorted(list(zip(passages, scores)), key=lambda x: x[1], reverse=True)
            return list(zip(passages, scores))
        # if passages is a dict, which in the format of {'file_name' : {'title': 'title', 'content': 'content'}}
        elif isinstance(passages, dict):
            scores = self.reranker.compute_score([[query, p.get('content')] for p in passages.values()], normalize=True)
            # print(scores)
            # in this case, we return the original dict with an additional key 'score'
            for i, key in enumerate(passages):
                passages[key]['score'] = scores[i]
                passages[key]['file_name'] = key
            return sorted(passages.values(), key=lambda x: x['score'], reverse=True)
        else:
            raise ValueError('Passages should be either a list of strings or a list of dicts.')
            

if __name__ == '__main__':
    #reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)
    doc_retrieval = DocRetrieval()
    # query = 'What is the capital of China?'
    # passages = ['Beijing is the capital of China.', 'Shanghai is the largest city in China.', 'The Great Wall is in China.']
    # results = doc_retrieval.retrieve(query, passages)
    # print(results)

    query = '2023年政府工作报告第一小节的内容是什么？'
    doc_loader = DocLoader()
    doc_content = doc_loader.load_doc() # a dict
    passages = doc_content
    results = doc_retrieval.retrieve(query, passages)
    for result in results:
        print(result['title'], result['score'])
        print(result['content'][:100])
        print('---')

