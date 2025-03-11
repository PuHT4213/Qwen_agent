import math
import torch

def cos_similarity(v1, v2):
    """计算两个向量的余弦相似度,v1和v2是两个tensors"""
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(v1, v2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0.0
    else:
        return dot_product / ((normA * normB) ** 0.5)

# test
if __name__ == '__main__':
    v1 = [1, 2, 3]
    v2 = [1, 2, 3]
    print(cos_similarity(v1, v2))  # 1.0

    v1 = [1, 2, 3]
    v2 = [3, 2, 1]
    print(cos_similarity(v1, v2))  # 0.7142857142857143

    v1 = [1, 2, 3]
    v2 = [0, 0, 0]
    print(cos_similarity(v1, v2))  # 0.0

    v1 = torch.tensor([1, 2, 3])
    v2 = torch.tensor([1, 2, 3])
    print(cos_similarity(v1, v2))  # 1.0