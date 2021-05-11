import logging
import random

from gensim.models import KeyedVectors
from collections import defaultdict


class W2V:

    def __init__(self, vec_path):
        self.logger = logging.getLogger(__name__)
        self.w2v = KeyedVectors.load_word2vec_format(vec_path, binary=False)
        self.cache_vec = defaultdict()
        self.emb_size = self.w2v.vector_size

    @classmethod
    def load_vec(cls, vec_path):
        return cls(vec_path)

    def generate_new_vector(self):
        return [random.uniform(-1, 1) for _ in range(self.emb_size)]

    def __getitem__(self, word):
        """
        TODO: 补充不在 w2v 中的情况，考虑最长匹配法来补充，特别是自定义的keywords
        """
        v = None
        if word is None:
            return None
        if word in self.cache_vec:
            return self.cache_vec[word]
        if word in self.w2v:
            v = self.w2v[word]
        if v is None:
            v = self.generate_new_vector()
        self.cache_vec[word] = v
        return v

    def __contains__(self, word):
        return word in self.w2v

    @property
    def vector_size(self):
        return self.w2v.vector_size


if __name__ == '__main__':
    w2v = W2V('../data/sgns.zhihu.word')
    print(w2v.vector_size)
    words =["MR4.5", "达希纳"]
    for word in words:
        if word in w2v:
            print(word)
        w2v[word]