import numpy as np

from util.jieba_tokenizer import Jieba_Tokenizer
from util.w2v import W2V

class Compute_Embedding(object):

    def __init__(self):
        self.w2v = None

    def init(self, w2v_path='data/vector.zhihu.word'):
        # 初始化 Jieba_Tokenizer
        # 初始化 Word2ev
        self.w2v = w2v = W2V(w2v_path)

    def compute(self, text):
        words = Jieba_Tokenizer.cut(text)
        vectors = []
        for word in words:
            vector = self.w2v[word]
            vectors.append(vector)
        text_vector = np.sum(np.array(vectors), axis=0)/len(vectors)
        return text_vector


compute_embedding = Compute_Embedding()
