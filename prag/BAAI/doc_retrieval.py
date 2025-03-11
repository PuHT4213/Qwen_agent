import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from FlagEmbedding import FlagReranker
from prag.docs.doc_loader import DocLoader

# example usage:
# reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation

# score = reranker.compute_score(['query', 'passage'])
# print(score) # -5.65234375

# # You can map the scores into 0-1 by set "normalize=True", which will apply sigmoid function to the score
# score = reranker.compute_score(['query', 'passage'], normalize=True)
# print(score) # 0.003497010252573502

# scores = reranker.compute_score([['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']])
# print(scores) # [-8.1875, 5.26171875]

# # You can map the scores into 0-1 by set "normalize=True", which will apply sigmoid function to the score
# scores = reranker.compute_score([['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']], normalize=True)
# print(scores) # [0.00027803096387751553, 0.9948403768236574]

class DocRetrieval:
    def __init__(self, reranker):
        self.reranker = reranker

    def retrieve(self, query, passages):
        scores = self.reranker.compute_score([[query, p] for p in passages], normalize=True)
        return sorted(list(zip(passages, scores)), key=lambda x: x[1], reverse=True)

if __name__ == '__main__':
    reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)
    doc_retrieval = DocRetrieval(reranker)
    query = 'What is the capital of China?'
    passages = ['Beijing is the capital of China.', 'Shanghai is the largest city in China.', 'The Great Wall is in China.']
    results = doc_retrieval.retrieve(query, passages)
    print(results)

    query = '2021年政府工作报告第一小节的内容是什么？'
    doc_loader = DocLoader()
    doc_content = doc_loader.load_doc()
    passages = list(doc_content.values())
    results = doc_retrieval.retrieve(query, passages)
    for passage, score in results:
        print(f'{score:.4f}: {passage[:20]}')
        print()

