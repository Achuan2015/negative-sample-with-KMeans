import os
import pickle
from data_indexer import data_indexer
from compute_embedding import compute_embedding
from k_means import K_Means

file_path = "data/faq_corpus_with_index.xlsx"
w2v_path = "data/vector.zhihu.word"
compute_embedding.init(w2v_path)

def get_corpus_vectors(inputs, compute_embedding):
    vectors = []
    for instance in inputs:
        vector = compute_embedding.compute(instance.content)
        vectors.append(vector)
        instance.vector = vector
    return vectors

if os.path.exists('data/inputs.pkl'):
    inputs = pickle.load(open('data/inputs.pkl', 'rb'))
else:   
    inputs = data_indexer.read(file_path)

if os.path.exists('data/vectors.pkl'):
    vectors = pickle.load(open('data/vectors.pkl', 'rb'))
else:
    vectors = get_corpus_vectors(inputs, compute_embedding)
    
y_pred = K_Means.fit_predict(vectors, n_cluster=256)