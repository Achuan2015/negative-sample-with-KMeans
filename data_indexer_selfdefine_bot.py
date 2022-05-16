from collections import defaultdict
import pandas as pd
from alias import Bot_Alias


class Data_Indexer(object):

    def __init__(self):
         self.corpus_id2intent_id = defaultdict()
         self.corpus_id2category = defaultdict()
         self.corpus_id2content = defaultdict()
         self.corpus_id2corpus = defaultdict()
         self.intent_id2corpus_id = defaultdict()

    def init(self, path):
        if path.endswith('xlsx'):
            dfs = pd.read_excel(path)
        else:
            dfs = pd.read_csv(path, sep='\t')

        self.corpus_id2intent_id = dict(zip(dfs['corpus_id'], dfs['intent_id']))
        self.corpus_id2category = dict(zip(dfs['corpus_id'], dfs['category']))
        self.corpus_id2content = dict(zip(dfs['corpus_id'], dfs['text']))

        for intent_id in dfs['intent_id'].drop_duplicates().tolist():
            self.intent_id2corpus_id[intent_id] = dfs[dfs['intent_id'] == intent_id]['corpus_id'].tolist()

    def generate_inputs(self, path='data/bot_corpus_20220516.csv'):
        if path.endswith('xlsx'):
            dfs = pd.read_excel(path)
        else:
            dfs = pd.read_csv(path, sep='\t')
        dfs = dfs[['category', 'intent_id', 'corpus_id', 'text']]
        inputs = dfs.apply(lambda row: Bot_Alias(row['text'], row['corpus_id'], row['intent_id'], row['category']), axis=1).tolist()
        return inputs


data_indexer = Data_Indexer()