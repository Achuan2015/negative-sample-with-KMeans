from collections import defaultdict
import os
import pickle
import numpy as np
import pandas as pd
from sklearn import cluster
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
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
    
    def generate_with_one_by_one(self, file_path, rate=0.25, n_cluster=256, is_save=False):
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
    
    def generate_random_sample(self, values, inputs, rate):
        number = len(values) * rate
        sample = []
        positive_sample = []
        negative_sample = []
        count = 0
        while len(positive_sample) + len(negative_sample) <= number * 2:
            if count >= 1000000:
                print(f'cluster sample exceed max time, it contains:{len(values)}')
                break
            pair = np.random.choice(values, size=2, replace=False)
            pair_set = set(pair)
            if inputs[pair[0]].question_id == inputs[pair[1]].question_id:
                if len(positive_sample) <= number:
                    if pair_set not in positive_sample:
                        positive_sample.append(pair_set)
                        sample.append((inputs[pair[0]].content, inputs[pair[1]].content, 1))
            else:
                if len(negative_sample) <= number:
                    if pair_set not in negative_sample:
                        negative_sample.append(pair_set)
                        sample.append((inputs[pair[0]].content, inputs[pair[1]].content, 0))
            count +=1
        return sample        
            
              
    def generate_with_random_sample(self, file_path, rate=1, n_cluster=38, is_save=False):
        sample = []
        inputs = self.get_inputs(file_path)
        vectors = self.get_corpus_vectors(inputs)
        max_task_number = 10
        if os.path.exists('data/cluster_result.pkl'):
            with open('data/cluster_result.pkl', 'rb') as f:
                cluster_result = pickle.load(f)
            y_pred = cluster_result['y_pred']
            cluster_mapping = cluster_result['cluster_mapping']
        else:
            y_pred, cluster_mapping = self.fit_predict(vectors, n_cluster=n_cluster)
            with open('data/cluster_result.pkl', 'wb') as f:
                cluster_result = pickle.dump({'y_pred': y_pred, 'cluster_mapping': cluster_mapping}, f)
        print('begin to generate sample')
        with ProcessPoolExecutor(max_task_number) as exectuor:
            fs = {exectuor.submit(self.generate_random_sample, values, inputs, rate):cluster_id 
                                for cluster_id, values in cluster_mapping.items()}
            for future in as_completed(fs):
                cluster_id = fs[future]
                sample.extend(future.result())
                print(f'cluster_id:{cluster_id} generate sample finish')
        if is_save:
            dfs = pd.DataFrame(sample, columns=['query', 'candidate', 'label'])
            dfs.to_csv(f'output_data/huaxia_faq_{n_cluster}_{rate}_20220330.csv', index=False, sep='\t')
        return sample

                   
sample_generator = Sample_Generator()
