from collections import defaultdict
import os
import pickle
import numpy as np
import pandas as pd
from numpy.core.arrayprint import _none_or_positive_arg
from numpy.lib.shape_base import _make_along_axis_idx
from sklearn import cluster
from data_indexer import data_indexer
from compute_embedding import compute_embedding
from k_means import K_Means


class Sample_Generator(object):

    def __init__(self):
        self.compute_embedding = compute_embedding
        self.data_indexer = data_indexer
        self.cluster_points = defaultdict(list)

    def init(self, file_path, w2v_path):
        self.compute_embedding.init(w2v_path)
        self.data_indexer.init(file_path)
    
    def get_inputs(self, file_path):
        inputs = []
        if os.path.exists('data/inputs.pkl'):
            inputs = pickle.load(open('data/inputs.pkl', 'rb'))
        else:   
            inputs = self.data_indexer.generate_inputs(file_path)
            with open('data/inputs.pkl', 'wb') as fi:
                pickle.dump(inputs, fi)
        return inputs
    
    def get_corpus_vectors(self, inputs):
        vectors = []
        if os.path.exists('data/vectors.pkl'):
            vectors = pickle.load(open('data/vectors.pkl', 'rb'))
        else:
            for instance in inputs:
                vector = self.compute_embedding.compute(instance.content)
                vectors.append(vector)
                instance.vector = vector
            with open('data/vectors.pkl', 'wb') as fv:
                pickle.dump(vectors, fv)
        return vectors

    def fit_predict(self, vectors, n_cluster=10):
        y_pred = K_Means.fit_predict(vectors, n_cluster=n_cluster)
        cluster_mapping = defaultdict()
        for i in range(n_cluster):
            index = np.where(y_pred == i)[0]
            cluster_mapping[i] = list(index)
        return y_pred, cluster_mapping
    
    def generate(self, file_path, rate=0.25, n_cluster=256, is_save=False):
        """
        考虑到不同的问题学习的难度不一致，这一点会体现在对应问题的拓展问的个数上
        params: rate: 一个样本生成 正/副 样本对的个数占对应问题样本的比例
        """
        sample = []
        inputs = self.get_inputs(file_path)
        vectors = self.get_corpus_vectors(inputs)
        y_pred, cluster_mapping = self.fit_predict(vectors, n_cluster=n_cluster)
        for idx, input in enumerate(inputs):
            print('idx', idx)
            cluster_id = y_pred[idx]
            cluster_ques = cluster_mapping[cluster_id]
            alias_ques = self.data_indexer.get_alias_ques(input.question_id)
            num = int(len(alias_ques)/4)
            if input.alias_id in alias_ques:
                alias_ques.remove(input.alias_id)
            positive_candidates = self.generate_positie_sample(alias_ques, num)
            negative_candidates = self.generate_negative_sample(input, cluster_ques, inputs, num)
            positive_sample = [(input.content, self.data_indexer.get_alias(alias_id), 1) for alias_id in positive_candidates]
            negative_sample = [(input.content, self.data_indexer.get_alias(alias_id), 0) for alias_id in negative_candidates]
            sample.extend(positive_sample)
            sample.extend(negative_sample)
        if is_save:
            dfs = pd.DataFrame(sample, columns=['query', 'candidate', 'label'])
            dfs.to_csv('data/sample.csv', index=False, sep='\t')
        return sample
        
    def generate_positie_sample(self, alias_ques, num):
        candidates = np.random.choice(alias_ques, size=num, replace=False)
        return candidates

    def generate_negative_sample(self, input, cluster_ques, inputs, num):
        candidates = []
        question_id = input.question_id
        while len(candidates) < num:
            target = np.random.choice(cluster_ques)
            if inputs[target].alias_id not in candidates and inputs[target].question_id != question_id:
                candidates.append(inputs[target].alias_id)
        return candidates

                   
sample_generator = Sample_Generator()